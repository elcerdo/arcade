#!/usr/bin/env bash

set -u
set -e

scp dedibox:roms.tar.gz .
rm -rf roms
tar xzvf roms.tar.gz

