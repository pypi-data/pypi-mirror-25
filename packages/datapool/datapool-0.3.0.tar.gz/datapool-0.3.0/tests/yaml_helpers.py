# encoding: utf-8
from __future__ import print_function, division, absolute_import

import glob
from os.path import join, relpath

from datapool.errors import DataPoolException
from datapool.logger import logger
from datapool.landing_zone_structure import lookup_pattern


def load(parser_func, landing_zone):

    root_folder = landing_zone.root_folder
    logger().info("use {} to parse all files from {}".format(parser_func.__name__, root_folder))
    results = []
    pattern = lookup_pattern(parser_func)
    try:
        for path in glob.glob(join(root_folder, pattern)):
            rel_path = relpath(path, start=root_folder)
            results.extend(parser_func(root_folder, rel_path))
        exceptions, valid_objects = split(results)
    except DataPoolException as e:
        logger().error(e)
        exceptions, valid_objects = [e], []

    return exceptions, valid_objects


def split(results):
    exceptions = [item for item in results if isinstance(item, Exception)]
    valid_objects = [item for item in results if not isinstance(item, Exception)]
    return exceptions, valid_objects
