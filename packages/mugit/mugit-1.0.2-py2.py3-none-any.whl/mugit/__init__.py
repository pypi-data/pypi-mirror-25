"""
mugit

This package contains objects used to manage a workspace containing
multiple git repositories.  Each object is represented by a class and
contained in a separate module in the package.

The object classes in the commands list are special in that they are designed
to be used by the mugit command-line tool to take command-line arguments
and use them to perform a specific operation on the workspace and/or its
git repositories, as defined by the command.

Copyright (c) 2017 Richard Walters
"""

from manifest import Manifest
from repository import Repository

from add import Add
from pull import Pull
from select import Select
from status import Status
from release import Release
from remove import Remove
from update import Update

version = "1.0.2"

commands = {
    "add": Add,
    "pull": Pull,
    "select": Select,
    "status": Status,
    "release": Release,
    "remove": Remove,
    "update": Update,
}
