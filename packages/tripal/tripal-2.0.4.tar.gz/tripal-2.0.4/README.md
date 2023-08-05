# Tripal Library

[![Build](https://travis-ci.org/galaxy-genome-annotation/python-tripal.svg?branch=master)](https://travis-ci.org/galaxy-genome-annotation/python-tripal)
[![Documentation](https://readthedocs.org/projects/python-tripal/badge/?version=latest)](http://python-tripal.readthedocs.io/en/latest/?badge=latest)

A Python library for interacting with [Tripal](http://tripal.info/)

## History

 - 2.0.4
    - Small bug fixes

 - 2.0.3
    - More reliable detection of job failures

 - 2.0.2
    - Fix broken pip install tripal

 - 2.0.1
    - Fix missing requirements

 - 2.0
    - Rewritten most of the code, now working in a similar way as parsec or chakin
    - New cli tool named 'tripaille'
    - Tripal jobs can now be run directly by python-tripal and stdout and stderr are retrieved at the end of jobs.
    - Updated indexing code to latest tripal_elasticsearch module

 - 1.9
    - Wait for job completion and get logs

## Requirements

The [tripal_rest_api](http://github.com/abretaud/tripal_rest_api) module needs to be installed on your tripal instance.

## License

Available under the MIT License
