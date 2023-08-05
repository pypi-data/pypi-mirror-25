"""
status.py

This command is used to generate a report on the state of
the workspace, typically one line per repository.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import os
import subprocess
import sys

from manifest import Manifest
from repository import Repository

class Status:
    description = "generate report on the state of the workspace"

    @staticmethod
    def PrintUsage():
        print("usage: mugit status [-q|--quiet] [-a|--all] [-l] [-c]")
        print("   or: mugit status -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("    -q          Don't print extra information while running")
        print("    --quiet     Don't print extra information while running")
        print("    -a          Show status of all repositories, even unchanged ones")
        print("    --all       Show status of all repositories, even unchanged ones")
        print("    -l          Local status only; don't check remotes")
        print("    -c          Use colorama")
        print("")
        print("Generate a report on the state of the workspace.")
        print("")
        print("The report is one line per repository, with the root workspace included")
        print("at the top, indicated by path \".\".  Refer to the following example to")
        print("understand the markings used.")
        print("")
        print(" -- + : new repository")
        print("/   - : missing repository")
        print("|   * : repository changed branches")
        print("| -- ? : upstream unknown")
        print("|/   ! : fetch needed")
        print("|| -- ^ : pinned (locked to a commit)")
        print("||/  -- repository path  -- A: added files")
        print("||| /      -- branch    / -- D: deleted files")
        print("||| |     /             |/ -- M: modified files")
        print("||| |     |             ||/ -- U: untracked files")
        print("||| |     |             |||/   -- local/remote commits")
        print("||| |     |             ||||  /")
        print(" !  .     master        A  U")
        print("+?  foo   master          M")
        print("-   bar   1.0")
        print("  ^ libs  master")
        print("    spam  master(main)    M   [2]")
        print("")
        print("If local and remote branch names differ, remote branch name is shown first,")
        print("followed by local branch in parenthesis.")
        print("")
        print("\"MERGING\" or \"REBASING\" is printed for any repositories that are currently")
        print("being merged or rebased.")
        print("")
        print("Local/remote commits shows whether the local branch is ahead or behind the")
        print("remote branch, or if they have diverged, and by how many commits.")
        print("A positive number indicates the local branch is ahead of the remote.")
        print("A negative number indicates the local branch is behind the remote.")
        print("Two numbers separated by a dash indicate the local and remote branches have")
        print("diverged, with the first number being the number of local commits, and the")
        print("second number being the number of remote commits, since the base of the two.")

    @staticmethod
    def __call__(args):
        needHelp = False
        verbose = True
        showAll = False
        checkRemotes = True
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
                    elif option == "--all":
                        showAll = True
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
                        elif option == 'a':
                            showAll = True
                        elif option == 'l':
                            checkRemotes = False
                        elif option == 'c':
                            useColorama = True
                        else:
                            unknownOptions.append(option)
        if needHelp:
            Status.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            print("")
            Status.PrintUsage()
            return 1
        if useColorama:
            import colorama
            colorama.init()
        manifest = Manifest.FromWorkspace()
        if verbose:
            print("manifest: %s" % (manifest.name))
            print("")
            sys.stdout.flush()
        manifest.repositories.insert(0, Repository.FromInspection(manifest.root, "."))
        knownRepositoriesByPath = {}
        for repository in manifest.repositories:
            knownRepositoriesByPath[repository.path] = repository
        newRepositoriesByPath = {}
        missingRepositoryPaths = set(knownRepositoriesByPath.keys())
        changedRepositoryPaths = set([])
        if verbose:
            print("")
        for dirpath, dirnames, filenames in os.walk(manifest.root):
            normdirpath = os.path.normpath(dirpath)
            path = os.path.relpath(normdirpath, manifest.root).replace('\\', '/')
            if verbose:
                line = "Scanning for repositories: %s" % (path)
                if len(line) < 78:
                    line = "%-78s" % (line)
                else:
                    line = "%s...%s" % (line[:65], line[-10:])
                print("\033[A%s" % (line))
                sys.stdout.flush()
            if ".git" in dirnames:
                repository = Repository.FromInspection(manifest.root, path)
                if path in knownRepositoriesByPath:
                    missingRepositoryPaths.remove(path)
                    if (
                        (
                            (repository.branch is not None)
                            and (repository.branch != knownRepositoriesByPath[path].branch)
                        )
                        or (repository.revision != knownRepositoriesByPath[path].revision)
                        or (
                            (repository.url is not None)
                            and (repository.url != knownRepositoriesByPath[path].url)
                        )
                    ):
                        knownRepositoriesByPath[path].branch = repository.branch
                        knownRepositoriesByPath[path].revision = repository.revision
                        knownRepositoriesByPath[path].url = repository.url
                        changedRepositoryPaths.add(path)
                else:
                    newRepositoriesByPath[path] = repository
                    manifest.repositories.append(repository)
                if dirpath == manifest.root:
                    dirnames.remove(".git")
                else:
                    del dirnames[:]
        if verbose:
            print("\033[A" + " " * 78)
            sys.stdout.flush()
        for repository in manifest.repositories:
            if verbose:
                line = "Determining branch label: %s" % (repository.name)
                if len(line) < 78:
                    line = "%-78s" % (line)
                else:
                    line = "%s...%s" % (line[:65], line[-10:])
                print("\033[A%s" % (line))
                sys.stdout.flush()
            if (
                (not repository.path in missingRepositoryPaths)
                and (repository.localBranch != repository.branch)
            ):
                repository.branchLabel = "%s(%s)" % (repository.branch, repository.localBranch)
            else:
                repository.branchLabel = repository.branch or "???"
        if verbose:
            print("\033[A" + " " * 78)
            sys.stdout.flush()
        maxNameLength = max([len(repository.name) for repository in manifest.repositories])
        maxBranchLabelLength = max([len(repository.branchLabel) for repository in manifest.repositories])
        originalWorkingDirectory = os.getcwd()
        for repository in sorted(manifest.repositories, lambda x,y: cmp(x.path, y.path)):
            if verbose:
                line = "Checking for changes: %s" % (repository.name)
                if len(line) < 78:
                    line = "%-78s" % (line)
                else:
                    line = "%s...%s" % (line[:65], line[-10:])
                print("\033[A%s" % (line))
                sys.stdout.flush()
            changes = False
            present = True
            presenceSpecifier = ' '
            remoteSpecifier = ' '
            pinSpecifier = ' '
            difference = ""
            if repository.path in newRepositoriesByPath:
                presenceSpecifier = '+'
                changes = True
            elif repository.path in missingRepositoryPaths:
                presenceSpecifier = '-'
                changes = True
                present = False
            elif repository.path in changedRepositoryPaths:
                presenceSpecifier = '*'
                changes = True
            if present:
                try:
                    os.chdir(os.path.join(manifest.root, repository.path))
                    remoteTrackingBranch = None
                    if (
                        (repository.localBranch is not None)
                        and (repository.url is not None)
                    ):
                        remoteTrackingBranch = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "%s@{u}" % (repository.localBranch)], stdout=subprocess.PIPE).communicate()[0].strip()
                    if (
                        checkRemotes
                        and (repository.localBranch is not None)
                        and (repository.url is not None)
                    ):
                        remote = subprocess.Popen(["git", "config", "branch.%s.remote" % repository.localBranch], stdout=subprocess.PIPE).communicate()[0].strip()
                        branchOnRemote = remoteTrackingBranch[len(remote)+1:]
                        us = subprocess.Popen(["git", "rev-parse", remoteTrackingBranch], stdout=subprocess.PIPE).communicate()[0].strip()
                        them = subprocess.Popen(["git", "ls-remote", repository.url, branchOnRemote], stdout=subprocess.PIPE).communicate()[0].strip().split()[0]
                        if us != them:
                            changes = True
                            remoteSpecifier = '!'
                    else:
                        remoteSpecifier = '?'
                    adds = False
                    deletes = False
                    modifications = False
                    untracked = False
                    for statusLine in subprocess.Popen(["git", "status", "--porcelain"], stdout=subprocess.PIPE).communicate()[0].strip().splitlines():
                        if statusLine.startswith("A"):
                            changes = True
                            adds = True
                        elif statusLine.startswith("D"):
                            changes = True
                            deletes = True
                        elif (
                            statusLine.startswith("M")
                            or statusLine.startswith(" M")
                        ):
                            changes = True
                            modifications = True
                        elif statusLine.startswith("?"):
                            changes = True
                            untracked = True
                    difference = "%c%c%c%c" % (
                        adds and 'A' or ' ',
                        deletes and 'D' or ' ',
                        modifications and 'M' or ' ',
                        untracked and 'U' or ' '
                    )
                    if os.path.exists(".git/MERGE_HEAD"):
                        changes = True
                        difference = "MERGING: " + difference
                    elif (
                        os.path.isdir(".git/rebase-merge")
                        or os.path.isdir(".git/rebase-apply")
                    ):
                        changes = True
                        difference = "REBASING: " + difference
                    if repository.revision is not None:
                        pinSpecifier = '^'
                    elif remoteTrackingBranch is not None:
                        left, right = (int(count) for count in subprocess.Popen(["git", "rev-list", "--left-right", "--count", "%s...%s" % (repository.localBranch, remoteTrackingBranch)], stdout=subprocess.PIPE).communicate()[0].strip().split())
                        if left == 0:
                            if right > 0:
                                changes = True
                                difference += " [-%u]" % (right)
                        elif right == 0:
                            changes = True
                            difference += " [%u]" % (left)
                        else:
                            changes = True
                            difference += " [%u-%u]" % (left, right)
                finally:
                    os.chdir(originalWorkingDirectory)
            if verbose:
                print("\033[A" + " " * 78 + "\r", end='')
            if changes or showAll:
                print("%c%c%c %-*s  %-*s  %s" % (presenceSpecifier, remoteSpecifier, pinSpecifier, maxNameLength, repository.name, maxBranchLabelLength, repository.branchLabel, difference))
            if verbose:
                print("")
                sys.stdout.flush()
        return 0
