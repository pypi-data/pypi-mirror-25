"""
remove.py

This command is used to remove a repository from the workspace.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

from manifest import Manifest
import os
import sys

class Remove:
    description = "remove repositories from workspace"

    @staticmethod
    def PrintUsage():
        print("usage: mugit remove [--] <PATH>..")
        print("   or: mugit remove -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("")
        print("Remove repositories from the workspace.")
        print("")
        print("List the relative paths to the repositories to remove from the workspace.")

    @staticmethod
    def __call__(args):
        needHelp = False
        acceptingOptions = True
        unknownOptions = []
        paths = []
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
                paths.append(arg)
        if needHelp:
            Remove.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            print("")
            Remove.PrintUsage()
            return 1
        originalWorkingDirectory = os.getcwd()
        try:
            manifest = Manifest.FromWorkspace()
            os.chdir(manifest.root)
            knownRepositoriesByPath = {}
            for repository in manifest.repositories:
                knownRepositoriesByPath[repository.path] = repository
            if len(paths) == 0:
                print("error: no repositories specified")
                print("")
                Remove.PrintUsage()
                return 1
            changed = False
            for path in paths:
                if path in knownRepositoriesByPath:
                    manifest.repositories.remove(knownRepositoriesByPath[path])
                    try:
                        ignored = open(".gitignore", "rt").readlines()
                        with open(".gitignore", "wt") as gitignore:
                            for line in ignored:
                                if line.strip() != "/%s/" % (path):
                                    gitignore.write(line)
                    except Exception:
                        pass
                    changed = True
                    print("Removed repository \"%s\"." % (path))
                else:
                    print("Repository \"%s\" not in the manifest." % (path))
            if changed:
                open(os.path.join(manifest.root, manifest.name + ".xml"), "wt").write(manifest.ToXML())
        except Exception as exc:
            print("error: %s" % (str(exc)), file=sys.stderr)
            return 1
        finally:
            os.chdir(originalWorkingDirectory)
        return 0
