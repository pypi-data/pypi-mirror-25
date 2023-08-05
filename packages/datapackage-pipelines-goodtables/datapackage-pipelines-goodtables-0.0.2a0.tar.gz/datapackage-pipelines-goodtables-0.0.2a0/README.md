Goodtables validation plugin for datapackage-pipelines
======================================================

| |Travis|
| |Coveralls|
| |PyPi|
| |SemVer|
| |Gitter|

A
`datapackage-pipelines <https://github.com/frictionlessdata/datapackage-pipelines>`__
processor to validate tabular resources using
`goodtables <https://github.com/frictionlessdata/goodtables-py>`__.

Install
-------

::

    # clone the repo and install it with pip

    git clone https://github.com/frictionlessdata/datapackage-pipelines-goodtables.git
    pip install -e .

Usage
-----

Add the following to the pipeline-spec.yml configuration to validate
each resource in the datapackage. A report is outputted to the logger.

.. code:: yaml

      ...
      - run: goodtables.validate
        parameters:
            fail_on_error: True,
            reports_path: 'path/to/datapackage/reports',  # where reports will be written
            datapackage_reports_path: 'reports',  # relative to datapackage.json
            write_report: True,
            goodtables:
                <key>: <value>  # options passed to goodtables.validate()

-  ``fail_on_error``: An optional boolean to determine whether the
   pipeline should fail on validation error (default ``True``).
-  ``reports_path``: An optional string to define where Goodtables
   reports should be written (default is ``reports``).
-  ``datapackage_reports_path``: An optional string to define the path
   to the report, relative to the datapackage.json (see note below).
-  ``write_report``: An optional boolean to determine whether a
   goodtables validation report should be written to ``reports_path``
   (default is ``True``).
-  ``goodtables``: An optional object passed to
   ``goodtables.validate()`` to customise its behaviour. See
   ```goodtables.validate()`` <https://github.com/frictionlessdata/goodtables-py/#validatesource-options>`__
   for available options.

If reports are written, and ``datapackage_reports_path`` is defined, a
``reports`` property will be added to the datapackage, detailing the
path to the report for each resource:

.. code:: json

    ...
    "reports": [
        {
            "resource": "my-resource",
            "reportType": "goodtables",
            "path": "path/to/my-resource.json"
        }
    ]

It is recommended that ``datapackage_reports_path`` is used to define a
relative path, from the datapackage.json file, that represents where the
report was written. ``datapackage_reports_path`` does not define where
the reports will be written, but helps ensure a correct path is defined
in the ``reports`` property in datapackage.json. This is useful when the
pipeline concludes with a ``dump_to.path`` processor.

.. |Travis| image:: https://img.shields.io/travis/frictionlessdata/datapackage-pipelines-goodtables/master.svg
   :target: https://travis-ci.org/frictionlessdata/datapackage-pipelines-goodtables
.. |Coveralls| image:: http://img.shields.io/coveralls/frictionlessdata/datapackage-pipelines-goodtables/master.svg
   :target: https://coveralls.io/r/frictionlessdata/datapackage-pipelines-goodtables?branch=master
.. |PyPi| image:: https://img.shields.io/pypi/v/datapackage-pipelines-goodtables.svg
   :target: https://pypi.python.org/pypi/datapackage-pipelines-goodtables
.. |SemVer| image:: https://img.shields.io/badge/versions-SemVer-brightgreen.svg
   :target: http://semver.org/
.. |Gitter| image:: https://img.shields.io/gitter/room/frictionlessdata/chat.svg
   :target: https://gitter.im/frictionlessdata/chat
