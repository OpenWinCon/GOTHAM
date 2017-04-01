# encoding: utf-8

import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def check_dependency():
    # dependencies can be any iterable with strings,
    # e.g. file line-by-line iterator
    dependencies = [
      'pymongo>=3.4.0',
      'pycrypto>=2.6.0',
      'psutil>=5.2.0',
      'pika>=0.9.0',
    ]

    # here, if a dependency is not met, a DistributionNotFound or VersionConflict
    # exception is thrown.
    pkg_resources.require(dependencies)

if __name__ == "__main__":
    check_dependency()