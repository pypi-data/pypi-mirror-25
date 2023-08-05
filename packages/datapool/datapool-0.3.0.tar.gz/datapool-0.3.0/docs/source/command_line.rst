Command line tools
===================

Example: Setting up the first landing zone
------------------------------------------

1. Initialization
~~~~~~~~~~~~~~~~~


First we create a folder ``/data`` to hold the landing zone, then we run the
``init-config`` command. The actual path to the landing zone is not fixed and
can be chosen arbitrarily.  As the ``init-config`` command  writes to ``/etc``
this command must be excecuted with appropriate access rights:

.. code-block:: bash

	$ sudo mkdir -p /data
	$ sudo pool init-config /data/landing_zone

	> init-config
	- guess settings
	- created config files at /etc/datapool
	  please edit these files and adapt the data base configuration to your setup
	+ initialized landing zone at /data/landing_zone

``init-config`` tries to detect ``R``, ``Python``, ``Julia`` and ``Matlab``
interpreters if installed and sets up the ``/etc/datapool/datapool.ini``
configuration file. 

2. Configuration
~~~~~~~~~~~~~~~~

Next we have edit the configuration file from the previous step and adapt it to
your database settings.

- For a postgres database server the connection string (database URL) is
  ``postgresql://user:password@127.0.0.1:5432/databasename``,
- Without a password protection it is
  ``postgresql://user@127.0.0.1:5432/databasename``
- For all other databases check
  `the sqlalchemy documentation <http://docs.sqlalchemy.org/en/latest/core/engines.html>`_

Running ``check-config`` will test entries in ``datapool.ini`` being valid:

.. code-block:: bash

	$ pool check-config

	> check-config
	- check settings in config file /etc/datapool/datapool.ini
	- try to connect to db
	- connected to db
	- check R configuration + code execution
	- check matlab configuration + code execution
	- check julia configuration + code execution
	- check python configuration + code execution
	+ all checks passed


3. Setting up a development landing zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sites, sensors or conversion scripts must not be created or edited within the
landing zone. Instead we first create a local copy called *development landing
zone* where one implements modifications and extensions until being faultless.

.. code-block:: bash

	$ pool start-develop ~/development_landing_zone

	> start-develop
    - operational landing zone is empty. create development landing zone with example files.
	- setup development data base
	- create tables and indices
	+ setup done



This development landing zone now contains example files specifying meta data
as well as example conversion scripts.

To check if the given example scripts work run

.. code-block:: bash

	$ pool check ~/development_landing_zone

	> check
	- check yaml files in landing zone at dlz
	- copy meta data from productive db
	- copy table comment
	- copy table parameter
	...
	- load and check 7 new yaml files:
	- dlz/data/parameters.yaml
	- dlz/data/sensor_from_company_xyz/source_type.yaml
	- dlz/data/sensor_from_company_xyz/sensor_instance_julia/source.yaml
	- dlz/data/sensor_from_company_xyz/sensor_instance_matlab/source.yaml
	- dlz/data/sensor_from_company_xyz/sensor_instance_python/source.yaml
	- dlz/data/sensor_from_company_xyz/sensor_instance_r/source.yaml
	- dlz/sites/example_site/site.yaml
	- all yaml files checked
	- check scripts landing zone at dlz
	- check data/sensor_from_company_xyz/sensor_instance_julia/conversion.jl
	- wrote conversion result to /tmp/tmppgkmdi2c/sensor_instance_julia_0.csv
	- wrote conversion result to /tmp/tmppgkmdi2c/sensor_instance_julia_0.txt
	- check data/sensor_from_company_xyz/sensor_instance_python/conversion.py
	- wrote conversion result to /tmp/tmppgkmdi2c/sensor_instance_python_0.csv
	- wrote conversion result to /tmp/tmppgkmdi2c/sensor_instance_python_0.txt
	- check data/sensor_from_company_xyz/sensor_instance_r/conversion.r
	- wrote conversion result to /tmp/tmppgkmdi2c/sensor_instance_r_0.csv
	- wrote conversion result to /tmp/tmppgkmdi2c/sensor_instance_r_0.txt
	- all scripts checked
	+ congratulations: all checks succeeded.



In case you have not all supproted interpreters some checks will fail. You can remove examples
scripts if you do not plan to use some of the supported programming languages.


Reference
---------

.. program-output:: pool init-config --help

.. program-output:: pool check-config --help

.. program-output:: pool init-db --help

.. program-output:: pool check --help

.. program-output:: pool start-develop --help

.. program-output:: pool update-operational --help

