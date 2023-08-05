"""
repository.py

This module defines the Repository class.

Copyright (c) 2017 Richard Walters
"""

import os
import subprocess

class Repository:
    def __init__(self):
        self.root = None
        self.path = None
        self.url = None
        self.branch = None
        self.revision = None

    def __getattr__(self, name):
        if name == "localBranch":
            localBranch = None
            originalWorkingDirectory = os.getcwd()
            try:
                if self.path is not None:
                    os.chdir(os.path.join(self.root, self.path))
                if os.path.isdir(".git"):
                    headRef = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip() or "HEAD"
                    if headRef == "HEAD":
                        localBranch = self.branch
                    else:
                        localBranch = headRef
                self.localBranch = localBranch
            finally:
                os.chdir(originalWorkingDirectory)
            return localBranch
        elif name == "remote":
            remote = None
            localBranch = self.localBranch
            originalWorkingDirectory = os.getcwd()
            try:
                if self.path is not None:
                    os.chdir(os.path.join(self.root, self.path))
                if os.path.isdir(".git"):
                    if localBranch is not None:
                        remote = subprocess.Popen(["git", "config", "branch.%s.remote" % localBranch], stdout=subprocess.PIPE).communicate()[0].strip() or None
                self.remote = remote
            finally:
                os.chdir(originalWorkingDirectory)
            return remote
        elif name == "name":
            if self.path == ".":
                return "(root)"
            else:
                return self.path
        else:
            raise AttributeError(name)

    @staticmethod
    def FromElement(root, element):
        repository = Repository()
        repository.root = root
        repository.path = element.attrib.get("path", None)
        repository.url = element.attrib.get("url", None)
        repository.branch = element.attrib.get("branch", None)
        repository.revision = element.attrib.get("revision", None)
        return repository

    @staticmethod
    def FromInspection(root, path):
        originalWorkingDirectory = os.getcwd()
        try:
            os.chdir(os.path.join(root, path))
            repository = Repository()
            repository.root = root
            repository.path = path
            if os.path.isdir(".git"):
                branch = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip() or "HEAD"
                if branch == "HEAD":
                    repository.revision = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip()
                    if repository.revision == "HEAD":
                        repository.revision = None
                    possibleBranches = subprocess.Popen(["git", "for-each-ref", "--contains", "HEAD", "refs/heads", "--format=%(refname:short)"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().splitlines()
                    if len(possibleBranches) == 1:
                        repository.branch = possibleBranches[0]
                    elif len(possibleBranches) > 1:
                        repository.possibleBranches = {}
                        for possibleBranch in possibleBranches:
                            url = None
                            remote = subprocess.Popen(["git", "config", "branch.%s.remote" % possibleBranch], stdout=subprocess.PIPE).communicate()[0].strip()
                            if len(remote) > 0:
                                url = subprocess.Popen(["git", "remote", "get-url", remote], stdout=subprocess.PIPE).communicate()[0].strip()
                            repository.possibleBranches[possibleBranch] = url
                else:
                    repository.branch = branch
                if repository.branch is not None:
                    repository.remote = subprocess.Popen(["git", "config", "branch.%s.remote" % repository.branch], stdout=subprocess.PIPE).communicate()[0].strip() or None
                    if repository.remote is not None:
                        repository.url = subprocess.Popen(["git", "remote", "get-url", repository.remote], stdout=subprocess.PIPE).communicate()[0].strip()
                        repository.localBranch = repository.branch
                        repository.branch = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "%s@{u}" % (repository.branch)], stdout=subprocess.PIPE).communicate()[0].strip()[len(repository.remote)+1:]
            return repository
        finally:
            os.chdir(originalWorkingDirectory)

    def ToXML(self, level):
        nextline = "\n" + ' ' * (level + 4)
        xml = ' ' * level + "<repository" + nextline
        if self.path is not None:
            xml += "path=\"%s\"" % (self.path) + nextline
        if self.url is not None:
            xml += "url=\"%s\"" % (self.url) + nextline
        if self.branch is not None:
            xml += "branch=\"%s\"" % (self.branch) + nextline
        if self.revision is not None:
            xml += "revision=\"%s\"" % (self.revision) + nextline
        xml += "/>\n"
        return xml
