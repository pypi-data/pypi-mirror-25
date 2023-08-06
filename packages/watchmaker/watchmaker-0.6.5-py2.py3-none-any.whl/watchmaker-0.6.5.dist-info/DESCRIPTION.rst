
.. image:: https://img.shields.io/github/license/plus3it/watchmaker.svg
   :target: ./LICENSE
   :alt: License


.. image:: https://travis-ci.org/plus3it/watchmaker.svg?branch=develop
   :target: https://travis-ci.org/plus3it/watchmaker
   :alt: Travis CI Build Status


.. image:: https://ci.appveyor.com/api/projects/status/github/plus3it/watchmaker?branch=develop&svg=true
   :target: https://ci.appveyor.com/project/plus3it/watchmaker
   :alt: AppVeyor Build Status


.. image:: https://img.shields.io/pypi/v/watchmaker.svg?label=version
   :target: https://pypi.python.org/pypi/watchmaker
   :alt: Latest Version


Watchmaker
==========

Applied Configuration Management

Overview
--------

Watchmaker is a Python package that helps bootstrap a vanilla OS image and
apply an OS configuration. Watchmaker itself reads a simple YAML configuration
file, which can be hosted on the local filesystem or on a web server.

Complex configuration management (CM) environments may be layered in as part of
the provisioning framework. Watchmaker includes a default configuration that
will install Salt and a handful Salt Formulas that can be used to harden a
system to DISA STIG standards, as well as integrate with common enterprise
services.

Documentation
-------------

For more information on installing and using Watchmaker, go to
https://watchmaker.readthedocs.io.


