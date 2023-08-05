# encoding: utf-8
from __future__ import print_function, division, absolute_import

from sqlalchemy.orm import sessionmaker

from .converters import domain_object_to_dbo
from .db_objects import SiteDbo
from .database import create_session
from .errors import ConsistencyError
from .logger import logger
from .utils import iter_to_list, update_and_report_change


def check_and_commit(site, engine):
    exceptions = check(site, engine)
    if exceptions:
        raise ConsistencyError("check for site update failed, see logs for details")
    return commit(site, engine)


def check_attributes(site):
    site_dbo = domain_object_to_dbo(site)
    for attribute_name in site:
        assert getattr(site_dbo, attribute_name) == site[attribute_name]


@iter_to_list
def check(site, engine):
    logger().debug("called check for site {}".format(site.name))
    session = create_session(engine)

    existing_site_dbo = session.query(SiteDbo).filter(SiteDbo.name == site.name).first()

    if existing_site_dbo is not None:
        logger().debug("site with same name {} already exists".format(existing_site_dbo))
        yield from _check_site_and_picture_modifications(existing_site_dbo, site, session)


@iter_to_list
def commit(site, engine):
    logger().info("called commit for site {}".format(site.name))
    session = create_session(engine)

    existing_site_dbo = session.query(SiteDbo).filter(SiteDbo.name == site.name).first()

    if existing_site_dbo is not None:
        logger().debug("site with same name {} already exists".format(existing_site_dbo))
        yield from _update(existing_site_dbo, site, session)
    else:
        site_row = domain_object_to_dbo(site)
        logger().debug("add new site row {}".format(site_row))
        session.add(site_row)

    session.commit()

    sites = session.query(SiteDbo).filter(SiteDbo.name == site.name).all()
    assert len(sites) == 1
    yield from sites


def _check_site_and_picture_modifications(site_dbo, site_from_landing_zone, session):

    yield from _check_for_site_modifications(site_dbo, site_from_landing_zone)

    (to_create, dbos_to_drop,
     dbos_already_existing) = _determine_picture_differences(site_dbo, site_from_landing_zone)

    yield from _handle_dropped_pictures(site_dbo, dbos_to_drop)
    yield from _check_picture_modifications(site_dbo, dbos_already_existing, site_from_landing_zone)


def _update(site_dbo, site_from_landing_zone, session):
    (to_create, dbos_to_drop,
     dbos_already_existing) = _determine_picture_differences(site_dbo, site_from_landing_zone)
    _add_new_pictures(site_dbo, to_create)

    # only allowed update on site:
    for name in ("description", "street", "city", "postcode"):
        yield from update_and_report_change(site_dbo, site_from_landing_zone, name, "site")

    lookup = {p.filename: p for p in site_from_landing_zone.pictures}
    for picture in site_dbo.pictures:
        yield from update_and_report_change(picture, lookup[picture.filename], "description", "site")


def _check_for_site_modifications(site_dbo, site_from_landing_zone):
    site = site_from_landing_zone
    if any((site_dbo.name != site.name, site_dbo.coord_x != site.coord_x,
            site_dbo.coord_y != site.coord_y, site_dbo.coord_z != site.coord_z)):
        from .pretty_printers import pretty_log  # local import avoids circular import
        error = logger().error
        error("detected site modifications. existing site:")
        pretty_log(error, site_dbo)
        error("detected site modifications. modified site:")
        pretty_log(error, site)
        yield ConsistencyError("detected invalid site modifiations, see log for details")


def _determine_picture_differences(site_dbo, site_from_landing_zone):

    # this all assumes that the picture file name is unique within one site:
    new_picture_names = {p.filename: p for p in site_from_landing_zone.pictures}
    existing_picture_names = {p.filename: p for p in site_dbo.pictures}

    names_to_create = set(new_picture_names) - set(existing_picture_names)
    names_to_drop = set(existing_picture_names) - set(new_picture_names)
    names_already_existing = set(existing_picture_names) & set(new_picture_names)

    to_create = list(map(new_picture_names.get, names_to_create))
    dbos_to_drop = list(map(existing_picture_names.get, names_to_drop))
    dbos_already_existing = list(map(existing_picture_names.get, names_already_existing))

    return to_create, dbos_to_drop, dbos_already_existing


def _handle_dropped_pictures(site_dbo, dbos_to_drop):
    if dbos_to_drop:
        logger().error("detected missing pictures in landing zone")
        for picture in sorted(dbos_to_drop, key=lambda p: p.filename):
            from .pretty_printers import pretty_log  # local import avoids circular import
            logger().error("picture removed from landing zone:")
            pretty_log(logger().error, picture)
        yield ConsistencyError("pictures removed from landing zone, see log for details")


def _check_picture_modifications(site_dbo, dbos_existing_pictures, site_from_landing_zone):
    new_pictures = {p.filename: p for p in site_from_landing_zone.pictures}
    old_picture_dbos = {p.filename: p for p in dbos_existing_pictures}

    invalid_updates = []
    common_names = new_pictures.keys() & old_picture_dbos.keys()
    for file_name in sorted(common_names):
        old_picture_dbo = old_picture_dbos[file_name]
        new_picture = new_pictures[file_name]
        are_same = _compare_pictures(old_picture_dbo, new_picture)
        if not are_same:
            invalid_updates.append((old_picture_dbo, new_picture))

    if invalid_updates:
        from .pretty_printers import pretty_log  # local import avoids circular import
        logger().error("detected not allowd modifications of pictures in landing zone:")
        for old_picture, new_picture in invalid_updates:
            logger().error("existing picture:")
            pretty_log(logger().error, old_picture)
            logger().error("modified picture:")
            pretty_log(logger().error, new_picture)

        yield ConsistencyError("detected invalid picture modification, see log for details")


def _compare_pictures(picture_dbo, new_picture):
    return all((picture_dbo.filename == new_picture.filename,
                picture_dbo.timestamp == new_picture.timestamp,
                picture_dbo.data == new_picture.data))


def _add_new_pictures(site_dbo, to_create):
    for picture in to_create:
        site_dbo.pictures.append(domain_object_to_dbo(picture))
