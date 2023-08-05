#!/bin/bash

# run reformatting code according to pep 8:

if yapf --version 2>/dev/null >/dev/null ; then
    yapf --style='{based_on_style: pep8, column_limit: 100}' --recursive -i -p datapool tests
    echo
    echo please run \"git diff\" to see the changes
else
    echo
    echo please run \"pip install yapf\" first
fi


