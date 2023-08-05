Eawag datapool data model
=========================

Legend:

-  ``pk`` = Primary Key
-  ``fk`` = Foreign Key
-  ``uq`` = Unique within table
-  A ``field`` in **bold letters** indicates a field which cannot be NULL

signal
------

This is the central table holding the measurements. Each row represents a *value* of a
*parameter* measured at a given *time* and location (*site*). The
coordinates of the signal may not correlate to entries in the `site` table.

+-------------------------+----------------+--------------------------------------------------------------+
| field                   | datatype       | description                                                  |
+=========================+================+==============================================================+
| **signal\_id**          | integer (pk)   |                                                              |
+-------------------------+----------------+--------------------------------------------------------------+
| **value**               | float          | the actual measured value of the parameter                   |
+-------------------------+----------------+--------------------------------------------------------------+
| **measurement\_date**   | date\_time     |  time when the value was measured.                           |
+-------------------------+----------------+--------------------------------------------------------------+
| **parameter\_id**       | integer (fk)   | parameter                                                    |
+-------------------------+----------------+--------------------------------------------------------------+
| **source\_id**          | integer (fk)   | source                                                       |
+-------------------------+----------------+--------------------------------------------------------------+
| **site\_id**            | integer (fk)   | site                                                         |
+-------------------------+----------------+--------------------------------------------------------------+
| coord\_x                | float          | at a given site, a signal may origin from a specific place   |
+-------------------------+----------------+--------------------------------------------------------------+
| coord\_y                | float          | the type of coordinate system is not defined                 |
+-------------------------+----------------+--------------------------------------------------------------+
| coord\_z                | float          | (may be defined later)                                       |
+-------------------------+----------------+--------------------------------------------------------------+

site
----

A site is a location where measurements are made. At a given site,
several measuring equipments (source) can be found. The location of the
site is also described by its coordinates.

+----------------+----------------+------------------------------------------------+
| field          | datatype       | description                                    |
+================+================+================================================+
| **site\_id**   | integer (pk)   |                                                |
+----------------+----------------+------------------------------------------------+
| **name**       | string (uq)    | Name of that site                              |
+----------------+----------------+------------------------------------------------+
| description    | string         |                                                |
+----------------+----------------+------------------------------------------------+
| street         | string         | street and number                              |
+----------------+----------------+------------------------------------------------+
| postcode       | string         | postal code                                    |
+----------------+----------------+------------------------------------------------+
| city           | string         |                                                |
+----------------+----------------+------------------------------------------------+
| country        | string         |                                                |
+----------------+----------------+------------------------------------------------+
| coord\_x       | float          | coordinates of a given site                    |
+----------------+----------------+------------------------------------------------+
| coord\_y       | float          | the type of coordinate system is not defined   |
+----------------+----------------+------------------------------------------------+
| coord\_z       | float          | (may be defined later)                         |
+----------------+----------------+------------------------------------------------+

picture
-------

Every site may contain a number of pictures. Filenames for each site
must be unique. The filetype (e.g. png, jpg, tiff) is determined by the filename 
extenion of the ``filename`` field.

+-------------------+----------------+---------------------------------------------+
| field             | datatype       | description                                 |
+===================+================+=============================================+
| **picture\_id**   | integer (pk)   |                                             |
+-------------------+----------------+---------------------------------------------+
| **site\_id**      | integer (fk)   | referring to the site                       |
+-------------------+----------------+---------------------------------------------+
| **filename**      | string         |                                             |
+-------------------+----------------+---------------------------------------------+
| description       | string         | additional information about the picture    |
+-------------------+----------------+---------------------------------------------+
| data              | blob           | contains the (binary) content of the file   |
+-------------------+----------------+---------------------------------------------+
| date              | date\_time     | creation date of the picture                |
+-------------------+----------------+---------------------------------------------+

source
------

A (data-) source is a specific measuring equipment. Every measurement
(**signal**) origins from a specific source. Sources are categorized
into **source\_types**. The name of a source must be unique.

+------------------------+----------------+--------------------------------------------------------------------------------+
| field                  | datatype       | description                                                                    |
+========================+================+================================================================================+
| **source\_id**         | integer (pk)   |                                                                                |
+------------------------+----------------+--------------------------------------------------------------------------------+
| **source\_type\_id**   | integer (fk)   | source category                                                                |
+------------------------+----------------+--------------------------------------------------------------------------------+
| site\_id               | integer (fk)   | optional reference to a site (may be NULL)                                     |
+------------------------+----------------+--------------------------------------------------------------------------------+
| **name**               | string (uq)    | Name of that source. Usually is a combination of source\_type and site name.   |
+------------------------+----------------+--------------------------------------------------------------------------------+
| description            | string         |                                                                                |
+------------------------+----------------+--------------------------------------------------------------------------------+
| serial                 | string         | serial number. Is unique, if available                                         |
+------------------------+----------------+--------------------------------------------------------------------------------+
| manufacturer           | string         | company which produced that equipment                                          |
+------------------------+----------------+--------------------------------------------------------------------------------+
| manufacturing\_date    | date\_time     | date when the equipment was manufactured                                       |
+------------------------+----------------+--------------------------------------------------------------------------------+

source\_type
------------

Categorization of a given source.

+------------------------+----------------+-----------------------+
| field                  | datatype       | description           |
+========================+================+=======================+
| **source\_type\_id**   | integer (pk)   | pk                    |
+------------------------+----------------+-----------------------+
| **name**               | string (uq)    | Name of that source   |
+------------------------+----------------+-----------------------+
| description            | string         |                       |
+------------------------+----------------+-----------------------+

special\_value\_definition
--------------------------

Certain source types produce categorical data, such as «dry», «wet»,
«n/a» and so on. This table is used *to correlate categorical data and numeric
values* for a given source type. For example the numerical value ``1`` might encode
the state «dry».

+--------------------------------------+----------------+--------------------------------------+
| field                                | datatype       | description                          |
+======================================+================+======================================+
| **special\_value\_definition\_id**   | integer (pk)   |                                      |
+--------------------------------------+----------------+--------------------------------------+
| **source\_type\_id**                 | integer (fk)   | source\_type                         |
+--------------------------------------+----------------+--------------------------------------+
| description                          | string         |                                      |
+--------------------------------------+----------------+--------------------------------------+
| **categorical\_value**               | string         | the catecorical value                |
+--------------------------------------+----------------+--------------------------------------+
| **numeric\_value**                   | float          | the numeric value it is mapped to.   |
+--------------------------------------+----------------+--------------------------------------+

parameter
---------

Every value in the **signal** table is connected to a specific parameter
which describes and defines its unit.

+---------------------+----------------+----------------------------------------------------+
| field               | datatype       | description                                        |
+=====================+================+====================================================+
| **parameter\_id**   | integer (pk)   |                                                    |
+---------------------+----------------+----------------------------------------------------+
| **name**            | string (uq)    | e.g. "rain intensity", "absorbance 200.00", etc.   |
+---------------------+----------------+----------------------------------------------------+
| description         | string         |                                                    |
+---------------------+----------------+----------------------------------------------------+
| **unit**            | string         | the physical unit, e.g. "mm/h", "m-1"              |
+---------------------+----------------+----------------------------------------------------+

parameter\_averaging
--------------------

Sometimes, data coming from a *source* comes already processed. For
example, the windspeed is the average speed during a certain time
period. These kind of information is parameter- and source-specific.

+--------------------------------+----------------+--------------------------------------------------------------------------------+
| field                          | datatype       | description                                                                    |
+================================+================+================================================================================+
| **parameter\_averaging\_id**   | integer (pk)   | not really necessary, since parameter\_id and source\_id together are unique   |
+--------------------------------+----------------+--------------------------------------------------------------------------------+
| **parameter\_id**              | integer (fk)   | parameter                                                                      |
+--------------------------------+----------------+--------------------------------------------------------------------------------+
| **source\_id**                 | integer (fk)   | source                                                                         |
+--------------------------------+----------------+--------------------------------------------------------------------------------+
| integration\_length\_x         | float          | data integration in meters                                                     |
+--------------------------------+----------------+--------------------------------------------------------------------------------+
| integration\_length\_y         | float          | data integration in meters                                                     |
+--------------------------------+----------------+--------------------------------------------------------------------------------+
| integration\_angle             | float          | data integration in degrees                                                    |
+--------------------------------+----------------+--------------------------------------------------------------------------------+
| integration\_time              | float          | data integration time in seconds                                               |
+--------------------------------+----------------+--------------------------------------------------------------------------------+

comment
-------

There are two types of signal annotations: comments and quality.
A comment is an arbitrary text, where as quality annotations have a
controlled vocabulary. A signal may contain more than one comment.

+-------------------+-----------------+----------------------------------------------------+
| field             | datatype        | description                                        |
+===================+=================+====================================================+
| **comment\_id**   | interger (pk)   |                                                    |
+-------------------+-----------------+----------------------------------------------------+
| **signal\_id**    | integer (fk)    |                                                    |
+-------------------+-----------------+----------------------------------------------------+
| **text**          | string          | the comment itself                                 |
+-------------------+-----------------+----------------------------------------------------+
| **timestamp**     | date\_time      | the time the comment was added                     |
+-------------------+-----------------+----------------------------------------------------+
| author            | string          | the username of the author who added the comment   |
+-------------------+-----------------+----------------------------------------------------+

signal\_quality
---------------

A signal may contain more than one quality flag (but not the same
quality flag twice). The combination of signal\_id and quality\_id
must be unique.

+---------------------------+----------------+---------------------------------------------------+
| field                     | datatype       | description                                       |
+===========================+================+===================================================+
| **signal\_quality\_id**   | integer (pk)   |                                                   |
+---------------------------+----------------+---------------------------------------------------+
| **signal\_id**            | integer (fk)   |                                                   |
+---------------------------+----------------+---------------------------------------------------+
| **quality\_id**           | integer (fk)   |                                                   |
+---------------------------+----------------+---------------------------------------------------+
| **timestamp**             | date\_time     | date when annotation was added                    |
+---------------------------+----------------+---------------------------------------------------+
| author                    | string         | username of the author who added the annotation   |
+---------------------------+----------------+---------------------------------------------------+

quality
-------

Measuring the environment is always error prone. This table holds the
controlled vacabulary mentioned above. As some quality flags may be assigned programatically
the *method* field indicates the origin of such an quality entry.

+-------------------+----------------+--------------------------------------------------+
| field             | datatype       | description                                      |
+===================+================+==================================================+
| **quality\_id**   | integer (pk)   |                                                  |
+-------------------+----------------+--------------------------------------------------+
| **flag**          | string (uq)    | a textual description of *quality_id*            |
+-------------------+----------------+--------------------------------------------------+
| method            | string         | a description how the quality flag is generated. |
+-------------------+----------------+--------------------------------------------------+


Design priniciples
-----------------------

The design of the database follows the https://en.wikipedia.org/wiki/Star_schema to model
multidimensional data with a https://en.wikipedia.org/wiki/Data_warehouse.

You find a graphical descripton of the star schema  :download:`here <./graphics/DataModel.svg>`.

We follow these  principles to assure a consistent layout of the underlying tables:

-  primary keys of a table are called ``tablename\_id`` instead of ``id``
-  table names are in singular
-  the star schema avoids too much normalization
-  a table should not contain too abstract information

