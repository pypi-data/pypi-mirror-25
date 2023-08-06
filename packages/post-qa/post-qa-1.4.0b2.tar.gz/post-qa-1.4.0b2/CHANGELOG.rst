##########
Change Log
##########

1.3.1 [2017-02-09]
==================

- Updated README 

1.3.0 [2017-02-09]
==================

- Upload validate_base blobs, measurement metadata and metric definitions to SQUASH
- --api-url cmd line option now points to SQUASH API root URL (e.g https://squash.lsst.codes/dashboard/api/)
- Removed --metrics cmd line option, metric definitions are upload dynamically now
- Added Travis set up for PyPI deployment

1.2.2 [2016-12-05]
==================

- Add --metrics CLI flag: allows us to customize what metrics are submitted from the command line invocation.
- Also removes AM3 from the default upload list.
- Omit measurements with None values from upload: needed for SQUASH API compatibility.
- Raise and print any requests exceptions when posting to the SQUASH API.
- Centralize dependencies in setup.py.

1.2.1 [2016-11-28]
==================

- Add ``--test`` option to print the shimmed JSON without uploading it.
- Update test JSON from ``validate_drp`` based on `DM-7933 <https://jira.lsstcorp.org/browse/DM-7933>`_.

1.2.0 [2016-10-15]
==================

- Update shims to work with `validate_base <https://github.com/lsst/validate_base>`_ -type Job JSON (as of `DM-7042 <https://jira.lsstcorp.org/browse/DM-7042>`_). The JSON created for SQUASH is unchanged.
- There is now a `schema <http://json-schema.org>`_ for the JSON submitted to SQUASH. See ``postqa/schemas/squash.json`` and the ``postqa.schemas`` module. Tests use this schema with the ``jsonschema`` package to validate output JSON.
- Improved tests and coverage.

`DM-7041 <https://jira.lsstcorp.org/browse/DM-7041>`_.

1.1.1 [2016-10-14]
==================

- GitHub repo URLs of packages are now obtained from ``lsstsw/etc/repos.yaml`` itself. Previously post-qa could not accurately describe packages not in the github.com/lsst GitHub organization.

`DM-6374 <https://jira.lsstcorp.org/browse/DM-6374>`_.

1.1.0 [2016-08-12]
==================

- Add additional Jenkins environment variables to support multiple datasets.

`DM-7098 <https://jira.lsstcorp.org/browse/DM-7098>`_.

1.0.0 [2016-07-01]
==================

- Initial release

`DM-6308 <https://jira.lsstcorp.org/browse/DM-6308>`_.
