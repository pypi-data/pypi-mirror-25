#!/bin/bash

# we inject an artifical etc folder for the config files, so we do not
# mess up a global config and we need no root priviliges to write the
# config files:

rm -rf etc
export ETC=./etc

LZ=./lz
DLZ=./dlz
DLZ2=./dlz2

rm -rf $LZ 2>/dev/null
rm -rf $DLZ 2>/dev/null
rm -rf $DLZ2 2>/dev/null

set -x

pool init-config --use-sqlitedb --force --force $LZ
pool init-db
pool check-config
pool start-develop $DLZ
pool run-simple-server
