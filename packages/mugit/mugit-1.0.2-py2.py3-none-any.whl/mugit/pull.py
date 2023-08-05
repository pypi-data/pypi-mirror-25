"""
pull.py

This command is used to clone repositories that are missing
in the workspace, and update those that are present so that
they have the latest changes from upstream.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import os
import subprocess
import sys

from manifest import Manifest
from repository import Repository

def PullRepository(repository):
    originalWorkingDirectory = os.getcwd()
    try:
        if os.path.isdir(os.path.join(repository.root, repository.path, ".git")):
            os.chdir(os.path.join(repository.root, repository.path))
            if os.path.exists(".git/MERGE_HEAD"):
                return "%s: skipping because it's being merged." % (repository.name)
            elif (
                os.path.isdir(".git/rebase-merge")
                or os.path.isdir(".git/rebase-apply")
            ):
                return "%s: skipping because it's being rebased." % (repository.name)
            if (
                (repository.revision is not None)
                or (repository.remote is None)
                or (repository.localBranch is None)
            ):
                return ""
            fetch = subprocess.Popen(["git", "fetch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = fetch.communicate()
            if fetch.returncode > 0:
                print(err, file=sys.stderr)
                raise Exception("error fetching %s" % (repository.name))
            remoteTrackingBranch = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "%s@{u}" % (repository.localBranch)], stdout=subprocess.PIPE).communicate()[0].strip()
            left, right = (int(count) for count in subprocess.Popen(["git", "rev-list", "--left-right", "--count", "%s...%s" % (repository.localBranch, remoteTrackingBranch)], stdout=subprocess.PIPE).communicate()[0].strip().split())
            if right > 0:
                rebase = subprocess.Popen(["git", "rebase", remoteTrackingBranch], stdout=subprocess.PIPE)
                rebase.communicate()
                if rebase.returncode > 0:
                    raise Exception("error rebasing %s" % (repository.name))
                if left > 0:
                    return (
                        "%s: rebased %d commit%s onto %d remote commit%s" % (
                            repository.name,
                            left,
                            's' if left != 1 else '',
                            right,
                            's' if right != 1 else ''
                        )
                    )
                elif right > 0:
                    return (
                        "%s: fast-forwarded %d commit%s" % (
                            repository.name,
                            right,
                            's' if right != 1 else ''
                        )
                    )
        else:
            os.chdir(repository.root)
            clone = subprocess.Popen(["git", "clone", repository.url, repository.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = clone.communicate()
            if clone.returncode > 0:
                print(err, file=sys.stderr)
                raise Exception("error cloning %s" % (repository.name))
            return "%s: cloned from %s" % (repository.name, repository.url)
        return ""
    finally:
        os.chdir(originalWorkingDirectory)

def Report(line):
    if len(line) > 0:
        print("\033[A" + " " * 78 + "\r", end='')
        print(line)
        print("")
        sys.stdout.flush()

class Pull:
    description = "clone missing repositories and fetch/rebase existing ones"

    @staticmethod
    def PrintUsage():
        print("usage: mugit pull [-c]")
        print("   or: mugit pull -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("    -c          Use colorama")
        print("")
        print("Clone missing repositories and fetch/rebase existing ones.")

    @staticmethod
    def __call__(args):
        needHelp = False
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
                    else:
                        unknownOptions.append(option)
                else:
                    for i in range(1, len(arg)):
                        option = arg[i]
                        if option in ['h', '?']:
                            needHelp = True
                        elif option == 'c':
                            useColorama = True
                        else:
                            unknownOptions.append(option)
        if needHelp:
            Pull.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            print("")
            Pull.PrintUsage()
            return 1
        if useColorama:
            import colorama
            colorama.init()
        manifest = Manifest.FromWorkspace()
        root = Repository.FromInspection(manifest.root, ".")
        print("Pulling: (root)")
        sys.stdout.flush()
        Report(PullRepository(root))
        manifest = Manifest.FromWorkspace()
        for repository in manifest.repositories:
            line = "Pulling: %s" % (repository.name)
            if len(line) < 78:
                line = "%-78s" % (line)
            else:
                line = "%s...%s" % (line[:65], line[-10:])
            print("\033[A%s" % (line))
            sys.stdout.flush()
            try:
                Report(PullRepository(repository))
            except Exception as exc:
                print("error: %s" % (str(exc)), file=sys.stderr)
                print("")
        print("\033[A" + " " * 78 + "\r", end='')
        return 0
