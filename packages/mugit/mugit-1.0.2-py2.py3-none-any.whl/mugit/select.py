"""
select.py

This command is used to select a manifest to use in other commands.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import os
import subprocess
import sys

from manifest import Manifest
from repository import Repository

class Select:
    description = "designate which workspace manifest to use"

    @staticmethod
    def PrintUsage():
        print("usage: mugit select [-n] [-q|--quiet] [-c] [--] <MANIFEST>")
        print("   or: mugit select -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("    -n          Don't move repository heads")
        print("    -q          Don't print extra information while running")
        print("    --quiet     Don't print extra information while running")
        print("    -c          Use colorama")
        print("")
        print("    MANIFEST    Name of manifest to use")
        print("")
        print("Select a manifest to use in other mugit commands.  Specify the manifest")
        print("using its name (name of manifest file, exluding \".xml\" part).")
        print("The selection is saved in the git configuration file (.git/config)")
        print("of the workspace.")
        print("")
        print("By default, the heads of repositories you already have that are listed")
        print("in the manifest are moved to match the manifest.  Use the -n option")
        print("to keep the repository heads where they are.")

    @staticmethod
    def __call__(args):
        needHelp = False
        acceptingOptions = True
        moveHeads = True
        verbose = True
        useColorama = False
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
                    elif option == "--quiet":
                        verbose = False
                    else:
                        unknownOptions.append(option)
                else:
                    for i in range(1, len(arg)):
                        option = arg[i]
                        if option in ['h', '?']:
                            needHelp = True
                        elif option == 'n':
                            moveHeads = False
                        elif option == 'q':
                            verbose = False
                        elif option == 'c':
                            useColorama = True
                        else:
                            unknownOptions.append(option)
            else:
                manifestName = arg
                break
        if needHelp:
            Select.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            Select.PrintUsage()
            return 1
        if manifestName is None:
            print("error: no manifest specified")
            print("")
            Select.PrintUsage()
            return 1
        try:
            subprocess.call(["git", "config", "--local", "mugit.manifest", manifestName])
            print("manifest selected: %s" % (manifestName))
            print("")
        except OSError as exc:
            print("error: could not run git: %s" % (exc.strerror), file=sys.stderr)
        if moveHeads:
            if useColorama:
                import colorama
                colorama.init()
            manifest = Manifest.FromWorkspace()
            if verbose:
                print("")
            originalWorkingDirectory = os.getcwd()
            for repository in manifest.repositories:
                if os.path.isdir(os.path.join(repository.root, repository.path, ".git")):
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
                    if inspection.remote is not None:
                        if repository.url != inspection.url:
                            report = "%s: URL %s -> %s" % (repository.name, inspection.url, repository.url)
                            try:
                                os.chdir(os.path.join(manifest.root, repository.path))
                                subprocess.call(["git", "remote", "set-url", repository.remote, repository.url])
                            finally:
                                os.chdir(originalWorkingDirectory)
                    if repository.revision is None:
                        if (
                            (inspection.branch is not None)
                            and (inspection.branch != repository.branch)
                        ):
                            changed = True
                            report = "%s: branch %s -> %s" % (repository.name, inspection.branch, repository.branch)
                            try:
                                os.chdir(os.path.join(manifest.root, repository.path))
                                subprocess.Popen(["git", "checkout", repository.branch], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                            finally:
                                os.chdir(originalWorkingDirectory)
                        elif inspection.revision is not None:
                            changed = True
                            report = "%s: unpinned from %s" % (repository.name, inspection.revision)
                            try:
                                os.chdir(os.path.join(manifest.root, repository.path))
                                subprocess.Popen(["git", "checkout", repository.branch], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                            finally:
                                os.chdir(originalWorkingDirectory)
                    elif inspection.revision != repository.revision:
                        changed = True
                        if inspection.revision is None:
                            report = "%s: pinned to %s" % (repository.name, repository.revision)
                        else:
                            report = "%s: revision %s -> %s" % (repository.name, inspection.revision, repository.revision)
                        try:
                            os.chdir(os.path.join(manifest.root, repository.path))
                            subprocess.Popen(["git", "checkout", repository.revision], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                        finally:
                            os.chdir(originalWorkingDirectory)
                    if report is not None:
                        if verbose:
                            print("\033[A" + " " * 78 + "\r", end='')
                        print(report)
                        if verbose:
                            print("")
                        sys.stdout.flush()
            if verbose:
                print("\033[A" + " " * 78 + "\r", end='')
        return 0
