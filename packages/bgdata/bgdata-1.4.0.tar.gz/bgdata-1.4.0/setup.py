import sys
from setuptools import setup, find_packages

if sys.hexversion < 0x02070000:
    raise RuntimeError('This package requires Python 2.7 or later.')

requires = ['bgconfig >= 0.2.0', 'homura >= 0.1.3']
if sys.hexversion < 0x03000000:
    requires += ['future']

# Remember to change the version at bgdata/utils.py too.
__version__ = '1.4.0'

setup(
    name="bgdata",

    version=__version__,

    packages=find_packages(),
    author='Barcelona Biomedical Genomics Lab',
    description="Simple data repository managment.",
    license="Apache License 2",
    keywords=["data", "managment", "repository"],
    url="https://bitbucket.org/bgframework/bgdata",
    download_url="https://bitbucket.org/bgframework/bgdata/get/"+__version__+".tar.gz",
    install_requires=requires,
    classifiers=[],
    package_data={'': ['*.template', '*.template.spec']},
    entry_points={
        'console_scripts': [
            'bg-data = bgdata.utils:cmdline',
            'bgdata = bgdata.utils:cmdline'
        ]
    }
)
