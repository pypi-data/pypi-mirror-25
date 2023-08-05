#!/usr/bin/env bash

coverage erase
coverage run --source datapool -m py.test
coverage report -m
coverage html
# coverage html -d docs/source/htmlcov
