# encoding: utf-8
from __future__ import print_function, division, absolute_import


def test_lookup():
    from datapool.landing_zone_structure import lookup_pattern, lookup_parser
    import datapool.yaml_parsers as parsers

    exceptions = ["parse_datetime"]

    for name, obj in parsers.__dict__.items():
        if name in exceptions:
            continue
        if name.startswith("parse_"):
            pattern = lookup_pattern(obj)
            assert pattern is not None, obj
            example_path = pattern.replace("*", "ABCD").replace("?", "Z")
            parser = lookup_parser(example_path)
            assert parser is not None, pattern
            assert parser == obj
