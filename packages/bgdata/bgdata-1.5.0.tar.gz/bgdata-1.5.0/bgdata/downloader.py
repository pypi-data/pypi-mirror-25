import datetime
import os
import sys
import tarfile

import logging
import time
from os.path import join, exists

import pycurl

import binascii
from homura import download
from bgconfig import BGConfig

from bgdata.errors import DatasetError

from requests import head, get
from requests.exceptions import RequestException


LATEST = 'latest'
logger = logging.getLogger(__name__)


class LocalRepository(object):

    def __init__(self, path, caches, offline=False):
        self.offline = offline
        self.path = os.path.expanduser(path)
        self.caches = [os.path.expanduser(c) for c in caches]
        self.last_error = None

    def get_latest(self, project, dataset, version):
        paths = [self.path] + self.caches
        for path in paths:
            package = join(path, project, dataset, "{}.latest".format(version))

            # Return latest build
            if exists(package):

                for retries in range(5):
                    try:
                        with open(package) as fd:
                            return fd.readlines()[0].strip()
                    except Exception as e:
                        self.last_error = e
                        # Wait one second and try again
                        time.sleep(1)
        return None

    def set_latest(self, project, dataset, version, build):

        if not self.offline and len(build) > 0:

            path = join(self.path, project, dataset, "{}.latest".format(version))
            try:
                with open(path, 'w') as fd:
                    fd.writelines([build])
            except OSError:
                # May be we are using a read only local repository
                pass

    def get_path(self, project, dataset, version, build):

        for path in self.caches:
            package = join(path, project, dataset, "{}-{}".format(version, build))
            if exists(join(package, ".downloaded")):
                return package

        package = join(self.path, project, dataset, "{}-{}".format(version, build))
        if exists(package):
            return package

        return package


class RemoteRepository(object):

    def __init__(self, url, proxy=None):
        self.url = url
        self.last_error = None
        self.proxy = {pycurl.FOLLOWLOCATION: 1}
        self.proxies = None

        if proxy is not None and 'host' in proxy:
            self.proxy[pycurl.PROXY] = proxy['host']
            self.proxies = {'http': "http://{}".format(proxy['host'])}

        if proxy is not None and 'port' in proxy:
            self.proxy[pycurl.PROXYPORT] = int(proxy['port'])
            self.proxies = {'http': "http://{}:{}".format(proxy['host'], proxy['port']) }

        if proxy is not None and 'user' in proxy and 'pass' in proxy:
            self.proxy[pycurl.PROXYUSERPWD] = "{}:{}".format(proxy['user'], proxy['pass'])
            self.proxies = {'http': "http://{}:{}@{}:{}".format(proxy['user'], proxy['pass'], proxy['host'], proxy['port']) }

    def get_latest(self, project, dataset, version, timeout=1.0):

        anticache = binascii.b2a_hex(os.urandom(15)).decode()
        latest_url = "{}/{}/{}/{}.latest?{}".format(self.url, project, dataset, version, anticache)
        try:
            r = get(latest_url, timeout=timeout, proxies=self.proxies)
            lines = r.content.splitlines()
            r.close()
            return lines[0].decode().strip()
        except RequestException as e:
            logging.debug("RemoteRepository.get_latest() error: {}".format(e))
            self.last_error = e
            return None

    def get_base_url(self, project, dataset, version, build):
        return "{}/{}/{}/{}-{}/package.tar".format(self.url, project, dataset, version, build)

    def check_url(self, url):
        try:
            h = head(url, proxies=self.proxies, allow_redirects=True)
            if h.status_code == 200:
                return True
        except RequestException:
            return False

        return False

    def download(self, dest, project, dataset, version, build, retries=3):

        # Download package
        logger.info("Downloading {}/{}/{}-{}".format(project, dataset, version, build))
        package_url = self.get_base_url(project, dataset, version, build)

        # Check compression format
        compression_format = None
        for cf in ["", ".gz", ".xz", ".bz2"]:
            if self.check_url(package_url + cf):
                compression_format = cf
                break

        # Package not found
        if compression_format is None:
            raise DatasetError(DatasetError.NOT_FOUND, 'Package {}/{}/{}-{} not found.'.format(project, dataset, version, build))

        # Make output directories
        if not exists(dest):
            os.makedirs(dest)

        # Package URL
        temp_file = join(dest, "package.tar" + compression_format)

        # Download
        logging.debug("Download URL: {}".format(package_url + compression_format))

        #try:
        download(package_url + compression_format, path=temp_file, pass_through_opts=self.proxy)
        #except Exception as e:
        #    raise DatasetError(DatasetError.DOWNLOAD_ERROR, "Download interrupted. ({})".format(e))

        # Extract package
        logger.info("Exctracting {}/{}/{}-{}".format(project, dataset, version, build))

        try:
            with tarfile.open(temp_file, 'r{}'.format(compression_format.replace('.', ':'))) as package:

                # Check if it's a single file
                names = package.getnames()

                if len(names) == 1:
                    # Create a file to mark this package as singlefile
                    with open(join(dest, '.singlefile'), 'w') as fd:
                        fd.writelines([names[0]])

                # Extract there
                package.extractall(dest)

                # Mark downloaded
                with open(join(dest, '.downloaded'), 'w') as fd:
                    fd.writelines([str(datetime.datetime.now())])
        except Exception as e:

            # If there was an error (ie. the file is corrupted)
            # remove the file
            logger.error("Error while extracting. {}".format(e))
            os.unlink(temp_file)

            if retries > 0:
                logger.info("Downloading again. Max retries: {}".format(retries))
                return self.download(dest, project, dataset, version, build, retries=retries-1)
            else:
                raise OSError(str(e))

        # Remove temporal file
        os.unlink(temp_file)

        logger.info("Package {}/{}/{}-{} ready".format(project, dataset, version, build))
        return True


class Downloader(object):

    def __init__(self, forceonline=False):

        self.config = BGConfig(os.path.join(os.path.dirname(__file__), "bgdata.conf.template"))
        self.offline = False if forceonline else self.config.get("offline", False)
        self.local = LocalRepository(os.environ.get("BGDATA_LOCAL", self.config['local_repository']), self.config['cache_repositories'], offline=self.offline)
        self.remote = RemoteRepository(os.environ.get("BGDATA_REMOTE", self.config['remote_repository']), proxy=self.config.get('proxy', None))
        self.warnings_build = set()
        self.warnings_path = set()

    def get_package_config(self, project, dataset, version):
        return self.config.get("{}/{}/{}".format(project, dataset, version), {})

    def get_latest(self, project, dataset, version):

        # Check custom build configuration
        custom_config = self.get_package_config(project, dataset, version)
        if 'build' in custom_config:
            key = "{}/{}/{}".format(project, dataset, version)
            if key not in self.warnings_build:
                logging.warning("BgData is using a custom build '{}' at {}".format(custom_config['build'], key))
                self.warnings_build.add(key)
            return custom_config['build']

        build = None
        build_local = self.local.get_latest(project, dataset, version)
        if not self.offline:
            # Get from remote repository
            timeout = 20.0 if build_local is None else 1.0
            build = self.remote.get_latest(project, dataset, version, timeout=timeout)

        # If we cannot get any latest from remote (may be we are offline)
        # use the local build
        if build is None:
            build = build_local

        # Raise an exception if we cannot discover the latest build
        if build is None:

            err_msg = "Package {}/{}/{}-? not available.".format(project, dataset, version)
            if self.remote.last_error is not None:
                err_msg += " ({})".format(self.remote.last_error)
            elif self.local.last_error is not None:
                err_msg += " ({})".format(self.local.last_error)

            raise DatasetError(DatasetError.UNKNOWN_LATEST_BUILD, err_msg)

        return build

    def is_downloaded(self, project, dataset, version, build=LATEST):

        # Get latest build
        latest = build == LATEST
        if latest:
            build = self.get_latest(project, dataset, version)

        local_path = self.local.get_path(project, dataset, version, build)

        downloaded = exists(join(local_path, '.downloaded'))

        if downloaded and latest:
            self.local.set_latest(project, dataset, version, build)

        return downloaded

    def get_path(self, project, dataset, version, build=LATEST, return_build=False):

        # Get latest build
        latest = build == LATEST
        if latest:
            build = self.get_latest(project, dataset, version)

        # Check if it has a custom folder
        package_config = self.get_package_config(project, dataset, version)
        if 'path' in package_config:
            key = "{}/{}/{}".format(project, dataset, version)
            if key not in self.warnings_path:
                logging.warning("BgData is using a custom path '{}' at {}".format(package_config['path'], key))
                self.warnings_path.add(key)

            if return_build:
                return package_config['path'], "custom"

            return package_config['path']

        # Check if it's at local
        local_path = self.local.get_path(project, dataset, version, build)

        if not exists(join(local_path, '.downloaded')):
            # Download it from remote
            try:
                self.remote.download(local_path, project, dataset, version, build)
            except OSError as e:
                logging.error("Impossible to download. {}".format(e))
                sys.exit(-1)

        # Check if it's a single file
        if exists(join(local_path, '.singlefile')):
            with open(join(local_path, '.singlefile')) as fd:
                file_name = fd.readlines()[0].strip()
                local_path = join(local_path, file_name)

        # Update latest
        if latest:
            self.local.set_latest(project, dataset, version, build)

        if return_build:
            return local_path, build

        return local_path
