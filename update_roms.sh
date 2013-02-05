#!/usr/bin/env bash

set -u
set -e

tar czvf roms.tar.gz roms/
scp roms.tar.gz dedibox:.

