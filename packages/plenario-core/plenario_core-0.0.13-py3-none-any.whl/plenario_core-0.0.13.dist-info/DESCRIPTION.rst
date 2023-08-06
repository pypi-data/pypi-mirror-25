Plenario Core
=============

.. image:: https://travis-ci.org/UrbanCCD-UChicago/plenario-core.svg?branch=master
   :target: https://travis-ci.org/UrbanCCD-UChicago/plenario-core

.. image:: https://coveralls.io/repos/github/UrbanCCD-UChicago/plenario-core/badge.svg?branch=master
   :target: https://coveralls.io/github/UrbanCCD-UChicago/plenario-core?branch=master

Usage
-----

*Coming Soon*


Development
-----------

Fire up a virtualenv and install the dev requirements::

    $ python3.6 -m venv .env
    $ source .env/bin/activate
    $ pip install -r dev-requirements.txt

To run the tests, in a separate terminal pull in the PostGIS docker image and create the database::

    $ docker pull mdillon/postgis
    $ docker run -d -p 5432:5432 mdillon/postgis
    $ docker ps
    ...
    $ docker exec -it {container hash} /bin/bash
    ...
    # su postgres -c psql
    ...
    > create database plenario;

Then all you have to do is run the tests normally::

    $ coverage run manage.py test
    $ coverage report
    $ flake8



