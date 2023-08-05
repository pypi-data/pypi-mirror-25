How to contribute to documentation
==================================

Initialization
--------------

To checkout the full repository, you need to configure ``git`` first.

.. code:: bash

    $ git clone https://ssdmsource.ethz.ch/uweschmitt/eawag_datapool.git
    $ cd eawag_datapool
    $ git branch --track docs origin/docs
    $ git checkout docs

Then install the packages needed to build the documentation:

.. code:: bash

    $ cd docs
    $ pip install -r requirements.txt

Typical workflow
----------------

Update your local repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To fetch the recent changes from other contributors first update your
local repository:

.. code:: bash

    $ git pull origin docs

Edit or add files
~~~~~~~~~~~~~~~~~

If you now edit the files in the ``sources`` folder or add a new file
you might want to include this into the table of contents. To do so you
have to add the new file(s) without their file extension to
``index.rst`` in the section starting with ``.. toctree::``.

After editing the files in ``docs/sources`` you can inspect the result
of your changes: First ``cd`` to the ``docs`` folder and run:

.. code:: bash

    $ make clean
    $ make html
    $ open build/html/index.html

Your browser should now show the current version of the documentation
web site.

Publish your changes
~~~~~~~~~~~~~~~~~~~~

To submit your changes first run ``git status`` to get an overview of
changed and new files.

Then execute

.. code:: bash

    $ git add PLACE_A_FILENAME_HERE

for all the files you added or changed. Then run

.. code:: bash

    $ git commit -m "PLACE A MESSAGE HERE DESCRIBING YOUR CHANGES"
    $ git push origin docs

After a few seconds you should see the changes published on
https://datapool.readthedocs.io.
