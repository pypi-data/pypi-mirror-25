"""
add.py

This command is used to add a repository to the workspace, either
by cloning it from a remote repository, or by locating it if
it's already present in the workspace.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import os
import sys

from manifest import Manifest
from repository import Repository

class Add:
    description = "add repositories to workspace"

    @staticmethod
    def PrintUsage():
        print("usage: mugit add [--] <PATH>..")
        print("   or: mugit add [-c] -a|--all")
        print("   or: mugit add -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("    -a          Add all repositories missing from manifest")
        print("    --all       Add all repositories missing from manifest")
        print("    -c          Use colorama")
        print("")
        print("Add repositories to the workspace manifest.")
        print("")
        print("List the relative paths to the repositories to add to the workspace manifest,")
        print("or use the -a|--all option to scan the workspace and add to the manifest")
        print("any repositories found that are not already listed in the manifest.")

    @staticmethod
    def __call__(args):
        needHelp = False
        acceptingOptions = True
        unknownOptions = []
        paths = []
        scan = False
        useColorama = False
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
                    elif option == "--all":
                        scan = True
                    else:
                        unknownOptions.append(option)
                else:
                    for i in range(1, len(arg)):
                        option = arg[i]
                        if option in ['h', '?']:
                            needHelp = True
                        elif option == 'a':
                            scan = True
                        elif option == 'c':
                            useColorama = True
                        else:
                            unknownOptions.append(option)
            else:
                paths.append(arg)
        if needHelp:
            Add.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            print("")
            Add.PrintUsage()
            return 1
        manifest = Manifest.FromWorkspace()
        knownRepositoriesByPath = {}
        for repository in manifest.repositories:
            knownRepositoriesByPath[repository.path] = repository
        if scan:
            if useColorama:
                import colorama
                colorama.init()
            print("")
            for dirpath, dirnames, filenames in os.walk(manifest.root):
                normdirpath = os.path.normpath(dirpath)
                path = os.path.relpath(normdirpath, manifest.root)
                line = "Scanning for repositories: %s" % (path)
                if len(line) < 78:
                    line = "%-78s" % (line)
                else:
                    line = "%s...%s" % (line[:65], line[-10:])
                print("\033[A%s" % (line))
                sys.stdout.flush()
                if dirpath == manifest.root:
                    dirnames.remove(".git")
                elif ".git" in dirnames:
                    if path not in knownRepositoriesByPath:
                        paths.append(path.replace('\\', '/'))
                    else:
                        del dirnames[:]
            print("\033[A" + " " * 78)
            sys.stdout.flush()
        elif len(paths) == 0:
            print("error: no repositories specified")
            print("")
            Add.PrintUsage()
            return 1
        changed = False
        originalWorkingDirectory = os.getcwd()
        try:
            for path in paths:
                if not os.path.isdir(os.path.join(path, ".git")):
                    raise Exception("not a git repository: %s" % (path))
                if path in knownRepositoriesByPath:
                    print("Repository \"%s\" is already in the manifest." % (path))
                else:
                    newRepository = Repository.FromInspection(manifest.root, path)
                    manifest.repositories.append(newRepository)
                    ignored = []
                    try:
                        ignored = open(".gitignore", "rt").readlines()
                    except Exception:
                        pass
                    ignored.insert(0, "/%s/\n" % (path))
                    open(".gitignore", "wt").writelines(ignored)
                    changed = True
                    print("Added repository \"%s\"." % (path))
            if changed:
                open(os.path.join(manifest.name + ".xml"), "wt").write(manifest.ToXML())
        finally:
            os.chdir(originalWorkingDirectory)
        return 0
