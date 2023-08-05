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
            fail_on_warn: False,
            suppress_if_valid: False,
            goodtables:
                <key>: <value>  # options passed to goodtables.validate()

-  ``fail_on_error``: An optional boolean to determine whether the
   pipeline should fail on validation error (default ``True``).
-  ``fail_on_warn``: An optional boolean to determine whether the
   pipeline should fail on validation warning (default ``False``).
-  ``suppress_if_valid``: An optional boolean to determine whether the
   goodtables validation report should be logged if there are no errors
   or warnings (default ``False``).
-  ``goodtables``: An optional object passed to
   ``goodtables.validate()`` to customise its behaviour. See
   ```goodtables.validate()`` <https://github.com/frictionlessdata/goodtables-py/#validatesource-options>`__
   for available options.

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
