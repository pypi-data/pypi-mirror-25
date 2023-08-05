Workflow example
================

To initialize ``datapool`` configuration on the current server run the ``init-config`` subcommand,
this might require admin permissions because the config file is stored in the ``/etc/datapool``
folder:

.. code-block:: bash

	$ pool init-config ./lz

	> init-config
	- guess settings
	  - 'matlab' not found on $PATH
	- created config files at /etc/datapool
	  please edit these files and adapt the data base configuration to your setup
	+ initialized landing zone at ./lz


Then edit this file and run ``pool check-config``:

.. code-block:: bash

	$ pool check-config

	> check-config
	- check settings in config file /etc/datapool/datapool.ini
	- try to connect to db
	- could not connect to db postgresql://user:password@localhost:5432/datapool
	- check R configuration + code execution
	- matlab not configured, skip tests
	- check julia configuration + code execution
	- check julia version.
	- check python configuration + code execution
	+ all checks passed


To start development create a so called *development landing zone** which can be an
arbitrary folder:

.. code-block:: bash

	$ pool start-develop ./dlz

	> start-develop
	- setup development landing zone
	- operational landing zone is empty. create development landing zone with example files.
	+ setup done


This copied some example ``.yaml`` files, conversion scripts and raw data files. To check
the scripts run:

.. code-block:: bash

	$ pool check-scripts ./dlz

	> check-scripts
	- check landing zone at ./dlz
	- check ./dlz/data/sensor_from_company_xyz/sensor_instance_julia/conversion.jl
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_julia_0.csv
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_julia_0.txt
	- check ./dlz/data/sensor_from_company_xyz/sensor_instance_python/conversion.py
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_python_0.csv
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_python_0.txt
	- check ./dlz/data/sensor_from_company_xyz/sensor_instance_r/conversion.r
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_r_0.csv
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_r_0.txt
	+ congratulations: checks succeeded.

This checked the scripts and you can inspect the results files as displayed in the output.

To check the ``.yaml`` files:

.. code-block:: bash

	$ pool check-yamls ./dlz/

	> check-yamls
	- check yamls in landing zone at ./dlz/
	- setup fresh development db. productive does not exist or is empty.
	- load and check 1 new yaml files:
	- ./dlz/data/parameters.yaml
	+ all yaml files checked

Now you can upload the changes from the development landing zone to the operational
landing zone:

.. code-block:: bash

	$ pool update-operational ./dlz

	> update-operational
	- check before copying files around.
	- copied data/parameters.yaml
	- copied data/sensor_from_company_xyz/sensor_instance_julia/conversion.jl
	- copied data/sensor_from_company_xyz/sensor_instance_julia/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/sensor_instance_matlab/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/sensor_instance_python/conversion.py
	- copied data/sensor_from_company_xyz/sensor_instance_python/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/sensor_instance_r/conversion.r
	- copied data/sensor_from_company_xyz/sensor_instance_r/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/source_type.yaml
	- copied sites/example_site/images/24G35_regenwetter.jpg
	- copied sites/example_site/images/IMG_0312.JPG
	- copied sites/example_site/images/IMG_0732.JPG
	- copied sites/example_site/site.yaml
	+ copied 13 files to ./lz

