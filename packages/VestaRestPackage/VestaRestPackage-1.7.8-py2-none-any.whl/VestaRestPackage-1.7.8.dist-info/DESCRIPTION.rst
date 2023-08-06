.. image:: https://travis-ci.org/crim-ca/RESTPackage.svg?branch=master

This package offers helper modules for exposing services working in a
distributed Service architecture through a REST interface. The work being
executed by these services might be an annotation process or a form of
conversion process taking a significant amount of time thereby benefiting from
a distributed processing system with a REST interface.

Messages are communicated through a `Celery <http://www.celeryproject.org/>`_
distributed processing queue system.

This package offers basic functionality yet is meant to be wrapped by a higher
level package which will offer a full application package.

Known examples of applications which use this package are:

* Vesta Load Balancer (alias Service Gateway or SG)
* Multimedia Storage System

Installation of this package can be done as follows::

   pip install VestaRestPackage


Release notes
=============

1.7.8
-----

* Configuration directive no_params_needed is now optionnal.

1.7.7
-----

* Handle error cases for JSON submittal with arguments.

1.7.6
-----

* Add configuration to service which permits use without any arguments.

1.7.5
-----

* Bug fix for error handling.

1.7.4
-----

* AMQP routes are explicitly specified when submitting tasks so that we can have a same task name on diffrent queues.

1.7.3
-----

* Work-around for PyPi package listing restriction. Functionnaly equivalent.

1.7.2
-----

* DB schema is now part of distributed package.

1.7.1
-----

* Log formatting. Default location of database relative to CWD by default.
* Add default entry point to print default configuration.

1.7.0
-----

* Packaged and uploaded to PyPi.


