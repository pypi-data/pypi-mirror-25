# encoding: utf-8

from functools import partial
import os
import sys

import click

print_ok = partial(click.secho)
print_err = partial(click.secho, fg="red")

start_pdb = False


@click.group()
@click.option("--pdb", is_flag=True, help="start python debugger in case of exceptions.")
def main(pdb):
    """the `pool` command provides sub commands to run imports from eawag data warehouse landing
    zones and supports test runs during development and integration of data sources
    """
    if pdb:
        global start_pdb
        start_pdb = True


def print_banner(function):
    def inner(*a, **kw):
        import inspect
        command_name = inspect.stack()[2].frame.f_locals.get("self").name
        print()
        click.secho("> {}".format(command_name), fg="blue")
        return function(*a, **kw)

    # click needs this to generate help texts from doc strings:
    inner.__doc__ = function.__doc__
    return inner


def inject_pdb(function):
    def inner(*a, **kw):
        try:
            return function(*a, **kw)
        except SystemExit:
            raise
        except:
            import pdb
            import traceback
            global start_pdb
            traceback.print_exc()
            if start_pdb or os.getenv("PDB"):
                type, value, tb = sys.exc_info()
                pdb.post_mortem(tb)
            else:
                print()
                print("set environment variable PDB to start debugger automatically.")
                sys.exit(1)

    # click needs this to generate help texts from doc strings:
    inner.__doc__ = function.__doc__
    return inner


@main.command("version")
def version():
    """prints current version of datapool software"""
    import datapool
    print("datapool {}".format(datapool.__version__))

@main.command("init-config")
@click.option("--verbose", is_flag=True, help="dumps lots of output from interaction with db")
@click.option('--use-sqlitedb', is_flag=True, help="use sqlite db")
@click.option(
    '--force', "force_count", count=True, help="use this twice to overwrite existing config files")
@click.argument("landing-zone-folder", type=str)
@print_banner
@inject_pdb
def init_config(verbose, landing_zone_folder, use_sqlitedb, force_count):
    """initializes /etc/datapool/ folder with config files.

    landing_zone_folder must be a non-existing folder on the current machine.
    """

    from .commands import init_config
    sys.exit(
        init_config(landing_zone_folder, use_sqlitedb, force_count > 1, print_ok, print_err,
                    verbose))


@main.command("check-config")
@click.option("--verbose", is_flag=True, help="dumps lots of output from interaction with db")
@print_banner
@inject_pdb
def check_config(verbose):
    """checks if config file(s) in /etc/datapool are valid.
    """
    from .commands import check_config
    sys.exit(check_config(print_ok, print_err, verbose))


@main.command("init-db")
@click.option("--verbose", is_flag=True, help="dumps lots of output from interaction with db")
@click.option('--force', "force_count", count=True, help="use this twice to overwrite existing db")
@print_banner
@inject_pdb
def init_db(verbose, force_count):
    """creates empty tables in operational database. Run check_config first to see if the configured
    data base settings are valid.
    """
    from .commands import init_db
    sys.exit(init_db(force_count > 1, verbose, print_ok, print_err))


@main.command("create-example")
@click.option('--force', 'force_count', count=True,
              help="use this twice to overwrite existing folder")
@click.argument("example-landing-zone-folder", type=str)
@print_banner
@inject_pdb
def create_example(example_landing_zone_folder, force_count):
    """setup landing zone in given folde with example files.
    """
    from .commands import create_example
    reset = (force_count > 1)
    sys.exit(create_example(example_landing_zone_folder, reset, print_ok, print_err))


@main.command("start-develop")
@click.option("--verbose", is_flag=True, help="dumps lots of output from interaction with db")
@click.option('--force', 'force_count', count=True, help="use this twice to overwrite existing db")
@click.argument("development-landing-zone-folder", type=str)
@print_banner
@inject_pdb
def start_develop(development_landing_zone_folder, force_count, verbose):
    """setup local landing zone for adding new site / instrument / conversion script. this command
    will clone the operational landing zone (might be empty).
    """
    from .commands import start_develop
    reset = (force_count > 1)
    sys.exit(start_develop(development_landing_zone_folder, reset, verbose, print_ok, print_err))


@main.command("update-operational")
@click.option("--verbose", is_flag=True, help="might dump lots of output")
@click.option(
    '--force',
    'force_count',
    count=True,
    help="use this twice to overwrite existing landing zone in case of errors when"
    " checking")
@click.argument("development-landing-zone-folder", type=str)
@print_banner
@inject_pdb
def update_operational(development_landing_zone_folder, force_count, verbose):
    """deploys local changes to operational landing zone.
    """
    from .commands import update_operational
    overwrite = (force_count > 1)
    sys.exit(
        update_operational(development_landing_zone_folder, verbose, overwrite, print_ok,
                           print_err))


@main.command("check")
@click.option('--result-folder', type=str, default=None, help="provide target for results")
@click.option("--verbose", is_flag=True, help="might dump lots of output")
@click.argument("development-landing-zone-folder", type=str)
@print_banner
@inject_pdb
def check(development_landing_zone_folder, result_folder, verbose):
    """checks scripts and produced results in given landing zone. does not write to database.
    """
    from .commands import check
    sys.exit(check(development_landing_zone_folder, result_folder, verbose, print_ok, print_err))


@main.command("run-simple-server")
@click.option("--verbose", is_flag=True, help="might dump lots of output")
@print_banner
@inject_pdb
def run_simple_server(verbose):
    """Runs single process datapool server. Mostly used for testing.
    """
    from .commands import run_simple_server
    sys.exit(run_simple_server(verbose, print_ok, print_err))
