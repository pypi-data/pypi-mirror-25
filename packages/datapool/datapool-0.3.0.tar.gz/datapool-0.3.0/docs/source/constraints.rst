Constraints
===========

This page lists constraints and requirements related to configuring and
running the ``datapool`` software.

Incoming data
-------------

Raw data files are written to the respective ``data/`` folders as
follows:

1. The new file ``data.incomplete`` is created and writing data to this
   file starts.

2. When the file content is complete the corresponding file handle is
   closed and the file is renamed to ``data-TIMESTAMP.raw``.

The actual format of ``TIMESTAMP`` is not fixed but must be unique and
as a string temporally ordered. Encoding a full date and time string
will help the users and developers to inspect and find files, especially
if present in the backup zone.

This procedure is called *write-rename pattern* and avoids conversion of
incomplete data files. The risk for such a race condition depends on the
size of the incoming data files and other factors and is probably very
low. But running a data pool over a longer time span increases this risk
and could result in missing data in the data base.


