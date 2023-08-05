import argparse
import logging
import sys

import bgdata


logger = logging.getLogger(__name__)


def cmdline():

    # Parse the arguments
    parser = argparse.ArgumentParser()

    # Mandatory
    parser.add_argument('project', help='Project name')
    parser.add_argument('dataset', help='Dataset name')
    parser.add_argument('version', help='Dataset version')
    parser.add_argument('-b', '--build', default=bgdata.LATEST, help='Dataset build (default latest)')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true', help="Give more information")
    parser.add_argument('-f', '--force', dest='force', default=False, action='store_true', help="Force to download the package even in offline mode")
    parser.add_argument('-q', '--quiet', dest='quiet', default=False, action='store_true', help="Show only the path (useful to use in a bash script)")
    parser.add_argument('--version', action='version', version="BgData version {}".format('1.4.0'))
    args = parser.parse_args()

    # Configure the logging
    if args.quiet:
        args.verbose = False

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG if args.verbose else logging.INFO)
    logger.debug(args)

    # Create a downloader
    downloader = bgdata.Downloader(forceonline=args.force)

    # Download the dataset
    try:
        dataset_path = downloader.get_path(args.project, args.dataset, args.version, build=args.build)
    except bgdata.DatasetError as e:
        logger.error(e.message)
        sys.exit(1)

    if not args.quiet:
        logger.info("Dataset downloaded")

    print(dataset_path)

if __name__ == "__main__":
    cmdline()

