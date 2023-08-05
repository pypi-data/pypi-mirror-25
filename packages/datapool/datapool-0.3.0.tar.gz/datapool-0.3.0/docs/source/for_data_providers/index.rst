Instructions for data provider
==============================

Data provider are usually scientist performing measurements in the field.


System Architecture
-------------------

Data flow model :download:`specification <../graphics/DataFlowModel.svg>`.


.. image:: ./../graphics/DataFlowModel.svg



Add Source Type
---------------

Add or Modify Parameters
~~~~~~~~~~~~~~~~~~~~~~~~

The file ``parameters.yaml`` is stored in the ``data`` folder and contains all the parameters. New parameters can be added here. The information to be included are:

- Name: Name of the Parameter

- Unit: Specifies the unit of the Parameter

- Description: Additional description of the parameter. In case there is no description required, the field can remain empty.

The syntax has to match the following example:

.. code-block:: YAML

    -
       name: Absorbance 202.50_nm
       unit: m-1
       description: absorbance at 202.50 nm wavelength

Add Site
--------

In order to add a new measuring site, the information about this site have to be provided as a ``site.yaml`` file in a new folder for the site, within the ``sites`` folder of the landingzone. The information to be specified are:

- Name: Name of the site

- Description: Free Text describing the particularities of the site

- Street, City and Coordinates: Specifying where the site is located

- Pictures (optional): Pictures relating to the site can be specified. Pictures are normally stored in the ``images`` folder of the specific site.

The structure of the file has to be the same as in the example below:

.. include:: site_example.rst


Add Source
----------

Conversion of raw data
----------------------

The files arriving in the landing zone are called *raw data*. Every
raw data file must be converted into a so called *standardized file* by
a conversion script. The format of the standardized files is defined
below. Typically, every source needs an individually adapted
conversion script.

Standardized file format
------------------------

The standardized file format for the input data is a ``csv`` file with
either six or for columns.


- File format: csv file with semicolon delimited (``;``)

- Data format: ``yyyy-mm-dd hh:mm:ss``

- Column names: The first row contains the column names. The first
  three are always: ``timestamp``, ``parameter``, ``value``. Next
  either the three columns ``x``, ``y``, ``z``, or the single column
  ``site`` must ist given.

- ``value`` column: Must contain only numerical values. Missing values
  (``NULL``, ``NA``, or similar) are not allowed.

- The coordinate columns may be empty.


Example standardized file format with coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


+---------------------+-----------------------+--------+--------+--------+-----+
| timestamp           | parameter             | value  | x      | y      | z   |
+=====================+=======================+========+========+========+=====+
| 2013-11-13 10:06:00 | Water Level           | 148.02 | 682558 | 239404 |     |
+---------------------+-----------------------+--------+--------+--------+-----+
| 2013-11-13 10:08:00 | Water Level           | 146.28 | 682558 | 239404 |     |
+---------------------+-----------------------+--------+--------+--------+-----+
| 2013-11-13 10:08:00 | Average Flow Velocity | 0.64   | 682558 | 239404 | 412 |
+---------------------+-----------------------+--------+--------+--------+-----+
| ...                 | ...                   | ...    | ...    | ...    |     |
+---------------------+-----------------------+--------+--------+--------+-----+

Example standardized file format with site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------------+-----------------------+--------+--------+
| timestamp           | parameter             | value  | site   |
+=====================+=======================+========+========+
| 2013-11-13 10:06:00 | Water Level           | 148.02 | zurich |
+---------------------+-----------------------+--------+--------+
| 2013-11-13 10:08:00 | Water Level           | 146.28 | zurich |
+---------------------+-----------------------+--------+--------+
| 2013-11-13 10:08:00 | Average Flow Velocity | 0.64   | zurich |
+---------------------+-----------------------+--------+--------+
| ...                 | ...                   | ...    | ...    |
+---------------------+-----------------------+--------+--------+


Conversion script
-----------------

The conversion script must define a function which reads raw data and write an output
file (a standardized file). The first argument if this function is the
path to the input raw data, the second argument the path to the resulting file.

The follwing points should be considered when writing an conversion script:

- Indicate corrupt input data by throwing an exception
  within a conversion script. A informative error message is helpful and will be logged.

- If a converson script writes to ``stdout`` (i.e. normal ``print()``
  commands) this may not appear in the datapool log file and thus
  might be overseen.

- All required third party modules, packages, or libraries must be
  installed globally. Do not try to install them within a script.


The following code snippets show how a conversion script
could look like for different languages.

R
~

.. include:: r_example.rst

Julia
~~~~~

- The function must be named ``convert``.
- The name of the julia file and the declared module must be the same (up to
  the ``.jl`` file extension). So the file containing the module
  ``conversion_lake_zurich`` must be saved as ``conversion_lake_zurich.jl``.
- Further the module and file name must be unique within the landing zone.

.. include:: julia_example.rst


Python
~~~~~~

.. include:: python_example.rst

Matlab
~~~~~~

- The function must be named ``conversion``.
- The file name must be named ``conversion.m``.


.. include:: matlab_example.rst
