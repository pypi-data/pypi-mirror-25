# encoding: utf-8
from __future__ import print_function, division, absolute_import

from fnmatch import fnmatch

from click.testing import CliRunner


def test_init_config(data_path, tmpdir, monkeypatch, regtest_list_folders):

    monkeypatch.setenv("ETC", tmpdir.strpath)
    from datapool.main import init_config

    runner = CliRunner()

    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    result = runner.invoke(init_config, [fresh_landing_zone])
    assert result.exit_code == 0, result.output

    regtest_list_folders(fresh_landing_zone, recurse=True)

    # try the same folder again:
    result = runner.invoke(init_config, [fresh_landing_zone])
    output = result.output.strip().split("\n")

    assert fnmatch(output[2], "*folder * already exists"), output
    assert result.exit_code == 1

    # try new folder, should fail because the datapool config folder was created before:
    non_existing_folder = tmpdir.join("landing_zone_0").mkdir().strpath
    result = runner.invoke(init_config, [non_existing_folder])

    output = result.output.strip()
    assert fnmatch(output, "*datapool folder * already exists"), output

    assert result.exit_code == 1


def test_init_db(data_path):

    from datapool.main import init_db

    runner = CliRunner()
    result = runner.invoke(init_db, [])
    assert result.exit_code == 0, result.output + str(result.exception)

    # should fail: can not init same db again
    runner = CliRunner()
    result = runner.invoke(init_db, [])
    assert result.exit_code == 1

    # should fail, one "--force" is not enough
    result = runner.invoke(init_db, ["--force"])
    assert result.exit_code == 1

    # should succed: we agree to overwrite existing db
    result = runner.invoke(init_db, ["--force", "--force"])
    assert result.exit_code == 0


def test_start_develop(data_path, tmpdir, monkeypatch):
    monkeypatch.setenv("ETC", tmpdir.strpath)

    from datapool.main import start_develop, init_config

    runner = CliRunner()

    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    result = runner.invoke(init_config, [fresh_landing_zone])
    assert result.exit_code == 0, result.output

    runner = CliRunner()
    result = runner.invoke(start_develop, [tmpdir.join("test_start_develop").strpath])
    assert result.exit_code == 0, result.output + str(result.exception)


def test_update_operational(data_path, tmpdir, monkeypatch):

    from datapool.main import update_operational, start_develop, init_config

    monkeypatch.setenv("ETC", tmpdir.strpath)

    runner = CliRunner()

    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    result = runner.invoke(init_config, [fresh_landing_zone])
    assert result.exit_code == 0, result.output

    result = runner.invoke(start_develop, [tmpdir.join("test_start_develop").strpath])
    assert result.exit_code == 0, result.output + str(result.exception)

    # no assert for return code. might fail or not depending on matlab availability
    runner.invoke(update_operational, [tmpdir.join("test_start_develop").strpath])


def test_check(data_path, tmpdir, monkeypatch):

    from datapool.main import check, start_develop, init_config

    monkeypatch.setenv("ETC", tmpdir.strpath)

    runner = CliRunner()

    fresh_landing_zone = tmpdir.join("landing_zone").mkdir().strpath
    result = runner.invoke(init_config, [fresh_landing_zone])
    assert result.exit_code == 0, result.output

    result = runner.invoke(start_develop, [tmpdir.join("test_start_develop").strpath])
    assert result.exit_code == 0, result.output + str(result.exception)

    # no assert for return code. might fail or not depending on matlab availability
    runner.invoke(check, [tmpdir.join("test_start_develop").strpath])
