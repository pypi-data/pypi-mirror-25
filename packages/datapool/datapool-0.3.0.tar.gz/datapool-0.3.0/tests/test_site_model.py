# encoding: utf-8
from __future__ import print_function, division, absolute_import

from functools import partial

import pytest

from datapool.yaml_parsers import parse_site
from datapool.database import setup_db, dump_db
from datapool.errors import ConsistencyError
from datapool.site_and_picture_model import check_and_commit
from datapool.pretty_printers import pretty_print

from .yaml_helpers import load

load_sites = partial(load, parse_site)


def test_load_valid_site(data_path, regtest, regtest_print, regtest_logger, lz):
    with regtest_logger():
        excs, sites = load_sites(lz)
    assert len(sites) == 1, excs
    site = sites[0]
    regtest_print("site object read from yaml:")
    pretty_print(site, file=regtest)
    assert not excs, str(excs)


def test_load_empty_site_yml(data_path, regtest_print, regtest_logger, lz):
    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/empty.yaml"))

    with regtest_logger():
        excs, sites = load_sites(lz)

    assert not sites
    assert excs
    for exc in excs:
        regtest_print(exc)


def test_load_image_file_missing(data_path, regtest_print, regtest_logger, lz, tmpdir):
    lz.remove_file("sites/example_site/images/1.jpg")

    with regtest_logger():
        excs, sites = load_sites(lz)
    assert not sites

    for exc in excs:
        regtest_print(str(exc).replace(tmpdir.strpath, "<tmpdir>"))


def test_commit_valid_site(data_path, regtest_logger, regtest, regtest_print, config, lz):

    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)
    assert not excs

    regtest_print("site object read from yaml:")
    pretty_print(site, file=regtest)

    with regtest_logger():
        (site_dbo,) = check_and_commit(site, engine)
    regtest_print()
    regtest_print("site row:", site_dbo)
    pretty_print(site_dbo, file=regtest)
    regtest_print()

    dump_db(config.db, file=regtest)


def test_commit_site_without_pictures(data_path, regtest, regtest_logger, config, lz):
    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/site_without_pictures.yaml"))

    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)
    assert not excs

    print("site object read from yaml:", file=regtest)
    pretty_print(site, file=regtest)

    with regtest_logger():
        (site_dbo,) = check_and_commit(site, engine)
    print(file=regtest)
    print("site row:", site_dbo, file=regtest)
    pretty_print(site_dbo, file=regtest)
    print(file=regtest)

    dump_db(config.db, file=regtest)


def test_commit_site_with_invalid_pictures(data_path, tmpdir, regtest_logger, regtest_print, lz):
    lz.overwrite_file("sites/example_site/site.yaml",
                      data_path("yamls/site_with_invalid_pictures.yaml"))

    with regtest_logger():
        excs, sites = load_sites(lz)

    assert not sites, "parsing should fail, picture data is invalid"

    for exc in excs:
        regtest_print(str(exc).replace(tmpdir.strpath, "<tmpdir>"))


def test_update_modified_site_yml(data_path, regtest, regtest_logger, config, lz):

    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)

    assert not excs, str(excs)

    print("site object read from yaml:", file=regtest)
    pretty_print(site, file=regtest)
    print(file=regtest)

    with regtest_logger():
        (site_dbo,) = check_and_commit(site, engine)

    print("site row after update:", site_dbo, file=regtest)
    pretty_print(site_dbo, file=regtest)
    print(file=regtest)

    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/site_modified.yaml"))
    with regtest_logger():
        excs, (site, ) = load_sites(lz)
    assert not excs, str(excs)

    print("site object read from yaml:", file=regtest)
    pretty_print(site, file=regtest)

    with pytest.raises(ConsistencyError) as e:
        with regtest_logger():
            check_and_commit(site, engine)

    print(file=regtest)
    print(e.value, file=regtest)
    print(file=regtest)

    dump_db(config.db, file=regtest)


def test_update_picture_removed(data_path, regtest, regtest_logger, config, lz):
    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)

        site_dbo, = check_and_commit(site, engine)
        print(site_dbo, file=regtest)

    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/site_picture_removed.yaml"))

    with regtest_logger():
        excs, (site, ) = load_sites(lz)

    with pytest.raises(ConsistencyError) as e:
        with regtest_logger():
            check_and_commit(site, engine)

    print(file=regtest)
    print(e.value, file=regtest)
    print(file=regtest)


def test_update_picture_added(data_path, regtest, regtest_logger, config, lz):
    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)
        assert not excs, str(excs)

        site_dbo, = check_and_commit(site, engine)
        print(site_dbo, file=regtest)

    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/site_picture_added.yaml"))
    lz.overwrite_file("sites/example_site/images/4.JPG", data_path("images/4.JPG"))

    with regtest_logger():
        excs, sites = load_sites(lz)
    assert not excs, str(excs)

    (site, ) = sites

    with regtest_logger():
        site_dbo, = check_and_commit(site, engine)

    pretty_print(site_dbo, file=regtest)


def test_update_picture_modified(data_path, regtest, regtest_logger, config, lz):
    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)
        assert not excs, str(excs)

        site_dbo, = check_and_commit(site, engine)
        print(site_dbo, file=regtest)

    lz.overwrite_file("sites/example_site/site.yaml", data_path("yamls/site_picture_modified.yaml"))

    with regtest_logger():
        excs, (site, ) = load_sites(lz)
    assert not excs, str(excs)

    with pytest.raises(ConsistencyError) as e:
        with regtest_logger():
            check_and_commit(site, engine)

    print(file=regtest)
    print(e.value, file=regtest)
    print(file=regtest)


def test_allowed_site_modifications(data_path, regtest, regtest_logger, config, lz):
    with regtest_logger():
        engine = setup_db(config.db)
        excs, (site, ) = load_sites(lz)
        assert not excs, str(excs)

        site_dbo, = check_and_commit(site, engine)
        print(site_dbo, file=regtest)

    lz.overwrite_file("sites/example_site/site.yaml",
                      data_path("yamls/site_allowed_modifications.yaml"))

    with regtest_logger():
        result = load_sites(lz)
        excs, (site, ) = load_sites(lz)
    assert not excs, str(excs)

    dbos = check_and_commit(site, engine)
    for dbo in dbos:
        print(dbo, file=regtest)

    dump_db(config.db, file=regtest)
