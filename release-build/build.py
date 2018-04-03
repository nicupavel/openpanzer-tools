#!/usr/bin/env python

#Copyright 2013 Nicu Pavel <npavel@mini-box.com>

import sys
import os
import importlib

from builder import  builder
from compiler import compiler

execpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "profiles")
platforms = [os.path.basename(d[0]) for d in os.walk(execpath)]
platforms = platforms[1:] # remove root "profiles" dir

if len(sys.argv) < 3:
    sys.exit("Usage %s <platform> <release|debug>. \nAvailable platforms: %s" % (sys.argv[0], platforms))

platform = sys.argv[1]
profile = sys.argv[2]

profileImport = "profiles." + platform + "." + profile
current = importlib.import_module(profileImport)

distro_files = []

builder.cleanup()
builder.add_javascript_settings(current.config)

if current.config["useCompiled"]:
    print "Compiling openpanzer.js"
    compiler.compile(current.config["rootDir"], "./compiler/", True)
    current.config["includeFiles"].append("js/openpanzer.js")
    os.remove('generated-prototypes.js')  # no longer needed don't include in zip
else:
    current.config["includeFiles"].append("js/")
    current.config["excludeFiles"].append("js/openpanzer.js")
    current.config["excludeFiles"].append("js/prototypes.js")  #will use the generated-prototypes.js

builder.generate_initial_filelist(current.config, distro_files)
builder.generate_index_html(current.config, profile)
builder.generate_game_content(current.config, distro_files)
builder.create_zip(current.config, distro_files)
builder.cleanup()

