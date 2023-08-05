"""
manifest.py

This module defines the Manifest class.

Copyright (c) 2017 Richard Walters
"""

import os
import subprocess
from xml.etree import ElementTree

from repository import Repository

class Manifest:
    def __init__(self):
        self.name = None
        self.root = None
        self.repositories = []

    @staticmethod
    def FromXML(root, xml):
        try:
            element = ElementTree.fromstring(xml)
        except Exception as exc:
            raise Exception("manifest corrupted: unable to parse XML: %s" % (exc.message))
        return Manifest.FromElement(root, element)

    @staticmethod
    def FromElement(root, element):
        if element.tag != "workspace":
            raise Exception("manifest corrupted: top element not workspace")
        manifest = Manifest()
        manifest.root = root
        repositories = element.find("repositories")
        if repositories is None:
            raise Exception("manifest corrupted: repositories not found")
        for subelement in repositories:
            manifest.repositories.append(Repository.FromElement(root, subelement))
        return manifest

    @staticmethod
    def FromWorkspace():
        root = None
        name = None
        try:
            root = os.path.normpath(subprocess.Popen(["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE).communicate()[0].strip())
            name = subprocess.Popen(["git", "config", "--local", "mugit.manifest"], stdout=subprocess.PIPE).communicate()[0].strip()
        except OSError as exc:
            raise Exception("could not run git: %s" % (exc.strerror))
        if len(name) == 0:
            raise Exception("no manifest selected")
        manifest = None
        try:
            xml = open(os.path.join(root, name + ".xml"), "rt").read()
            manifest = Manifest.FromXML(root, xml)
        except IOError as exc:
            manifest = Manifest()
        manifest.name = name
        manifest.root = root
        return manifest

    def ToXML(self):
        xml = "<?xml version=\"1.0\"?>\n"
        xml += "<workspace>\n"
        xml += "    <repositories>\n"
        for repository in sorted(self.repositories, lambda x,y: cmp(x.path, y.path)):
            xml += repository.ToXML(8)
        xml += "    </repositories>\n"
        xml += "</workspace>\n"
        return xml
