.. image:: https://img.shields.io/pypi/v/post-qa.svg
.. image:: https://img.shields.io/travis/lsst-sqre/post-qa.svg

#######
post-qa
#######

Upload metric definitions, measurements and blobs from `validate_drp <https://github.com/lsst/validate_drp>`_ to
the `SQuaSH API <https://github.com/lsst-sqre/qa-dashboard>`_. ``post-qa`` is meant to run in a CI workflow, like
LSST Data Management's Jenkins CI.

Install
=======

::

   pip install post-qa

Command Line Interface
======================

::

   usage: post-qa [-h] --lsstsw LSSTSW_DIRNAME --qa-json QA_JSON_PATH --api-url
                  API_URL --api-user API_USER --api-password API_PASSWORD [--test]

   Upload JSON from validate_drp to the SQuaSH API.

   This script is meant to be run from a Jenkins CI environment
   and uses the following environment variables:

   - ``BUILD_ID`` : ID in the ci system
   - ``BUILD_URL``: ci page with information about the build
   - ``PRODUCT``: the name of the product built, in this case 'validate_drp'
   - ``dataset``: the name of the dataset processed by validate_drp
   - ``label`` : the name of the platform where it runs


   optional arguments:
     -h, --help            show this help message and exit
     --lsstsw LSSTSW_DIRNAME
                           Path of lsstsw directory
     --qa-json QA_JSON_PATH
                           Filename of QA JSON output file
     --api-url API_URL     SQuaSH API root URL
     --api-user API_USER   Username for SQuaSH API
     --api-password API_PASSWORD
                           Password for SQuaSH API
     --test                Print the shimmed JSON rather than uploading it

Further Reading
===============

- `lsst.validate.base metric measurement framework <https://validate-base.lsst.io/>`_.
- `SQR-008: SQUASH QA database <http://sqr-008.lsst.io>`_.
- `SQR-009: SQUASH dashboard prototype <http://sqr-009.lsst.io>`_.

License Info
============

Copyright 2017 AURA/LSST

MIT licensed open source.