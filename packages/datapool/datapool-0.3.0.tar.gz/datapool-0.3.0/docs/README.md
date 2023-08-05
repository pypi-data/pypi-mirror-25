[![documentation](https://readthedocs.org/projects/datapool/badge/?version=latest)](https://datapool.readthedocs.io)

# datapool

This library provides functions and a commandline utility to import data form the landing zone
of EAWAG sensor data into the EAWAG sensor data warehouse.

The landing zone is strctured into different folders and data and data annotation is extracted
based on standardized test files and yaml files.

The current layout of the file system is:

 - sites/ folder constains subfolders with sites. In every sub folder a `sites.yaml` file
   discribes the site with additional pictures.

# Documentation
See [here](https://datapool.readthedocs.io).


# Installation

## How to setup a development environment

### Prerequisites

To run datapool, you need to have installed:

 * python 3.5 (https://www.python.org/downloads/)
 * sqllite 3 (https://sqlite.org/download.html)

Instead of downloading you can use a package manager. On **Mac OS X** you can use brew (visit http://brew.sh to install it)

     $ brew install python3
     $ brew install sqlite3

On **Ubuntu**, the standard package manager is called `apt-get`. You also need the python3-venv package.

     $ sudo apt-get install python3.5
     $ sudo apt-get install python3-venv
     $ sudo apt-get install sqlite3

### Clone the project and install it

Clone the project:

    $ cd
    $ git clone https://ssdmsource.ethz.ch/uweschmitt/eawag_datapool.git
    $ cd ~/eawag_datapool

Next we create a virtual environment for Python. See
http://docs.python-guide.org/en/latest/dev/virtualenvs/ why this is a good
idea. A virtual environment means that a copy of your system's Python installation is
made. Adapt the following line to make sure that the `-p` points to a Python 3.4 or Python 3.5
interpreter on your machine (this might not work if you use anaconda Python distribution, use
the official Python interpreter from your Linux distribution instead):

    $ virtualenv -p /usr/bin/python3.5 venv
    $ source venv/bin/activate

Notice that your prompt will (might) change to `(venv)`. (You can leave the
virtual environment by just typing `deactivate`. This puts you back to the
system’s default Python interpreter with all its installed libraries).

Download and install all the needed packages (listed in setup.py) as follows:

    (venv) $ pip install -e .

The `-e` flag means «editable» and creates links to the datapool Python files (instead of copying them). If you update datapool, the new files become available immediately.

After all the packages have been downloaded and successfully installed, the command `pool` is now available:

    (venv) $ pool --help
    Usage: pool [OPTIONS] COMMAND [ARGS]...
    ...

Now, run the tests:

    (venv) $ py.test -v

To execute a test run `pool` provides the `testrun` subcommand:

    (venv) $ pool testrun --help
    (venv) $ pool testrun tests/data/test_landing_zone


### Run datapool

Every time you want to run datapool, you need to switch to the virtual environment:

    $ cd ~/eawag_datapool
    $ source venv/bin/activate


### Update datapool

To fetch updates from this repository run

    $ cd ~/eawag_datapool
    $ git pull origin master
    $ pip install -e .
