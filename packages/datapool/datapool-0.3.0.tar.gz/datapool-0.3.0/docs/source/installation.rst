Installation
============

Setup on Ubuntu 16.04
---------------------


Run the following instructions as ``root``:


 1. Ubuntu packages

    .. code-block:: none

       $ apt install git
       $ apt install r-base
       $ apt install postgresql
       $ apt install python3-pip
       $ apt install python3-psycopg2


 2. Install julia 0.5.0: (Ubuntu offers jula 0.4.x only):

    .. code-block:: none

        $ wget https://julialang.s3.amazonaws.com/bin/linux/x64/0.5/julia-0.5.0-linux-x86_64.tar.gz
        $ tar xzf julia-0.5.0-linux-x86_64.tar.gz
        $ mv julia-3c9d75391c /opt
        $ ln -s /opt/julia-3c9d75391c/bin/julia /usr/local/bin/
        $ julia --version


 3.  Create data base user and database

    .. code-block:: none

        $ sudo -u postgres createuser -P datapool
        $ sudo -u postgres createdb -O datapool datapool


    Note choosen password, then check:

    .. code-block:: none

        $ psql -U datapool -h 127.0.0.1 datapool
        $ ^D    (control-D to exit postgress shell)


 4. Install datapoool

    .. code-block:: none

        $ cd /opt
        $ git clone https://ssdmsource.ethz.ch/uweschmitt/eawag_datapool.git
        $ pip3 install -e eawag_datapool


    Check installation:

    .. code-block:: none

        $ pool --help


    Install needed packages for demo scripts:

    .. code-block:: none

        $ /opt/eawag_datapool/scripts/setup_julia.sh
        $ /opt/eawag_datapool/scripts/setup_python.sh
        $ /opt/eawag_datapool/scripts/setup_r.sh


 5. Create user:

    .. code-block:: none

        $ addgroup datapool    # currently already exists.
        $ useradd -m -G datapool -s /bin/bash datapool-provider


    julia packages are installed per user, so we run installation for datapool-provider
    again:


    assign password, do not forget the :

    .. code-block:: none

        $ passwd datapool-provider


 6. Initalized datapool configuration and setup landing zone:

    We assume that the landing zone will be located on a shared drive mounted at ``/nfsmount``,
    but you are free to choose any other folder

    .. code-block:: none

        $ pool init-config /nfsmount/landing_zone
        $ mkdir -p /nfsmount/landing_zone

        $ chgrp -R datapool /nfsmount/landing_zone
        $ chmod -R g+w /nfsmount/landing_zone


 7. Adapt configuration:

    .. code-block:: none

        $ nano /etc/datapool/datapool.ini


    edit:

    .. code-block:: none

        ...
        connection_string = postgresql://datapool:PASSWORD_FROM_STEP_3@127.0.0.1:5432/datapool

        ...
        [backup_landing_zone]
        folder = /data/backup_landing_zone/


    check:

    .. code-block:: none

        $ pool check-config


 8.  Create service:

    .. code-block:: none

        $ ln -s /opt/eawag_datapool/scripts/datapool.service /etc/systemd/system
        $ systemctl daemon-reload


 9.  Start service:

    .. code-block:: none

        $ systemctl start datapool.service
        $ systemctl status datapool.service


 10.  Observe running service: 

    can be stopped with ^C), can be used without ``-f``:

    .. code-block:: none

        $ journalctl -u datapool -f

    Keep this terminal window open.

 11. First steps as data provider:

    Login as user ``datapool-provider`` first.

    Install needed Julia packages (these are installed per user):

    .. code-block:: none

        $ /opt/eawag_datapool/scripts/setup_julia.sh

    Now we can create a development landing zone:

    .. code-block:: none

        $ pool start-develop dlz

    and run the checks:

    .. code-block:: none

        $ pool check dlz

    This should indicate that matlab files can not be executed (unless you already
    have matlab installed on your system). We fix this and run the checks again:

    .. code-block:: none

        $ rm -rf dlz/data/sensor_from_company_xyz/sensor_instance_matlab/
        $ pool check dlz


    If this succeeds we try to push the example data to the operational landing zone:

    .. code-block:: none

        $ pool update-operational dlz

    You should now see the messages in the terminal window from step 10.
