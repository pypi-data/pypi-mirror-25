"""
update.py

This command is used to update the workspace manifest to match the
actual repositories present in the workspace, and the branches or
revisions checked out.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import os
import sys

from manifest import Manifest
from repository import Repository

class Update:
    description = "update manifest to reflect current workspace state"

    @staticmethod
    def PrintUsage():
        print("usage: mugit update [-q|--quiet] [-c]")
        print("   or: mugit update -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("    -q          Don't print extra information while running")
        print("    --quiet     Don't print extra information while running")
        print("    -c          Use colorama")
        print("")
        print("Update branch, revision, and URL of each repository in the manifest")
        print("to match the workspace.")

    @staticmethod
    def __call__(args):
        needHelp = False
        verbose = True
        useColorama = False
        unknownOptions = []
        for arg in args:
            if (
                (len(arg) >= 1)
                and (arg[0] == '-')
            ):
                if (
                    (len(arg) >= 2)
                    and (arg[1] == '-')
                ):
                    option = arg
                    if option == "--help":
                        needHelp = True
                    elif option == "--quiet":
                        verbose = False
                    else:
                        unknownOptions.append(option)
                else:
                    for i in range(1, len(arg)):
                        option = arg[i]
                        if option in ['h', '?']:
                            needHelp = True
                        elif option == 'q':
                            verbose = False
                        elif option == 'c':
                            useColorama = True
                        else:
                            unknownOptions.append(option)
        if needHelp:
            Update.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            print("")
            Update.PrintUsage()
            return 1
        if useColorama:
            import colorama
            colorama.init()
        manifest = Manifest.FromWorkspace()
        if verbose:
            print("manifest: %s" % (manifest.name))
            print("")
            sys.stdout.flush()
        changed = False
        if verbose:
            print("")
        for repository in manifest.repositories:
            if verbose:
                line = "Checking for changes: %s" % (repository.name)
                if len(line) < 78:
                    line = "%-78s" % (line)
                else:
                    line = "%s...%s" % (line[:65], line[-10:])
                print("\033[A%s" % (line))
                sys.stdout.flush()
            inspection = Repository.FromInspection(manifest.root, repository.path)
            report = None
            if inspection.branch != repository.branch:
                changed = True
                report = "%s: branch %s -> %s" % (repository.name, repository.branch, inspection.branch)
                repository.branch = inspection.branch
            if inspection.revision != repository.revision:
                changed = True
                if repository.revision is None:
                    report = "%s: pinned to %s" % (repository.name, inspection.revision)
                elif inspection.revision is None:
                    report = "%s: unpinned from %s" % (repository.name, repository.revision)
                else:
                    report = "%s: revision %s -> %s" % (repository.name, repository.revision, inspection.revision)
                repository.revision = inspection.revision
            if inspection.url is not None:
                if inspection.url != repository.url:
                    changed = True
                    report = "%s: URL %s -> %s" % (repository.name, repository.url, inspection.url)
                    repository.url = inspection.url
            if report is not None:
                if verbose:
                    print("\033[A" + " " * 78 + "\r", end='')
                print(report)
                if verbose:
                    print("")
                sys.stdout.flush()
        if verbose:
            print("\033[A" + " " * 78 + "\r", end='')
        if changed:
            open(os.path.join(manifest.root, manifest.name + ".xml"), "wt").write(manifest.ToXML())
        return 0
