Run server in test mode
=======================

The following sequence initializes  ``datapool`` and runs the server in single
process mode.

.. code-block:: bash

    $ rm -rf ./lz 2>/dev/null

    $ export ETC=./etc
    $ rm -rf $ETC 2>/dev/null

    $ pool init-config --use-sqlitedb ./lz
    $ pool init-db
    $ pool check-config
    $ pool run-simple-server


Usually ``pool init-config`` would write to ``/etc/datapool`` and thus the
command requires ``root`` privileges. Setting the environment variable ``ETC``
allows overriding the ``/etc`` folder so we do not interfere with a global
setup.

Further we use ``--use-sqlitedb`` so configuration and setup of a data base
system as Postgres is not required. This flag is introduced for testing, in
operational mode we recommond to avoid this flag and configer  Postgres
instead.

The last ``run-simple-server`` command will observe changes to the operational
landing zone at `./lz`  and report its operations. The command does not run in
the background and thus will block the terminal until the user presses ``CTRL-C``
to enforce shutdown.

As a data provider we open another terminal window, setup a development landing
zone and commit the defaults to the operational landing zone. You should then
see some output from the ``run-simple-server`` command in the previous terminal
window:

.. code-block:: bash

    $ rm -rf ./dlz 2>/dev/null
    $ export ETC=./etc

    $ pool start-develop dlz
    $ pool check dlz
    $ pool update-operational dlz
