"""
release.py

This command is used to create a new manifest for the workspace that lists
all repositories as pinned to their current head revisions.
This can be selected later to force the heads of all repositories in
the workspace back to where they were when the manifest was made.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import os
import subprocess
import sys

from manifest import Manifest
from repository import Repository

class Release:
    description = "create or update a release/snapshot manifest"

    @staticmethod
    def PrintUsage():
        print("usage: mugit release [--] <MANIFEST>")
        print("   or: mugit release -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("")
        print("    MANIFEST    Name of manifest to use")
        print("")
        print("Create or update a release/snapshot manifest.")
        print("")
        print("Select a manifest to create or update.  Specify the manifest")
        print("using its name (name of manifest file, exluding \".xml\" part).")

    @staticmethod
    def __call__(args):
        needHelp = False
        acceptingOptions = True
        unknownOptions = []
        manifestName = None
        for arg in args:
            if (
                acceptingOptions
                and (len(arg) >= 1)
                and (arg[0] == '-')
            ):
                if (
                    (len(arg) >= 2)
                    and (arg[1] == '-')
                ):
                    option = arg
                    if option == "--":
                        acceptingOptions = False
                    elif option == "--help":
                        needHelp = True
                    else:
                        unknownOptions.append(option)
                else:
                    for i in range(1, len(arg)):
                        option = arg[i]
                        if option in ['h', '?']:
                            needHelp = True
                        else:
                            unknownOptions.append(option)
            else:
                manifestName = arg
                break
        if needHelp:
            Release.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            Release.PrintUsage()
            return 1
        if manifestName is None:
            print("error: no manifest specified")
            print("")
            Release.PrintUsage()
            return 1
        manifest = Manifest.FromWorkspace()
        originalWorkingDirectory = os.getcwd()
        for repository in manifest.repositories:
            if repository.revision is None:
                try:
                    os.chdir(os.path.join(manifest.root, repository.path))
                    repository.revision = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE).communicate()[0].strip()
                finally:
                    os.chdir(originalWorkingDirectory)
        open(os.path.join(manifestName + ".xml"), "wt").write(manifest.ToXML())
        return 0
