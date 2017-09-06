#!/usr/bin/env python

import pathlib
THIS_DIR = pathlib.Path(__file__).parent

print THIS_DIR
print str(THIS_DIR.resolve())
