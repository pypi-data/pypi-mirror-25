#! /usr/bin/env python

"""
main.py

This is a command-line tool used to execute mugit command objects.
It interprets the first command line argument as the name of the
mugit command to execute, looks up the named command, and executes it,
delegating to it the remainder of the command line.

Copyright (c) 2017 Richard Walters
"""

from __future__ import print_function

import mugit
import os
import re
import subprocess
import sys

def PrintUsage():
    print("usage: mugit <COMMAND> [ARGUMENT]..")
    print("   or: mugit <COMMAND> -h|-?|--help")
    print("   or: mugit -v|--version")
    print("   or: mugit -h|-?|--help")
    print("")
    print("    -h          Print usage information and exit")
    print("    -?          Print usage information and exit")
    print("    --help      Print usage information and exit")
    print("    -v          Print version information and exit")
    print("    --version   Print version information and exit")
    print("")
    print("commands:")
    for commandName in sorted(mugit.commands):
        command = mugit.commands[commandName]
        print("    %-10s  %s" % (commandName, command.description))
    print("")
    print("Use -h, -?, or --help without a command to see this usage information.")
    print("Use -h, -?, or --help with a command to see usage information")
    print("specific to that command.")

def Main(argv):
    print("")
    needHelp = False
    showVersion = False
    unknownOptions = []
    commandName = None
    commandArgs = []
    for argc in range(1, len(argv)):
        arg = argv[argc]
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
                elif option == "--version":
                    showVersion = True
                else:
                    unknownOptions.append(option)
            else:
                for i in range(1, len(arg)):
                    option = arg[i]
                    if option in ['h', '?']:
                        needHelp = True
                    elif option == 'v':
                        showVersion = True
                    else:
                        unknownOptions.append(option)
        else:
            commandName = arg
            commandArgs = argv[argc+1:]
            break
    if needHelp:
        PrintUsage()
        return 0
    if showVersion:
        gitVersion = None
        try:
            gitVersionLine = subprocess.Popen(["git", "version"], stdout=subprocess.PIPE).communicate()[0].strip()
            gitVersionPattern = re.compile("(?:\d+)\.(?:\d+)(?:\.\d+)?")
            gitVersion = ", git " + gitVersionPattern.search(gitVersionLine).group()
        except OSError as exc:
            print("error: could not run git: %s" % (exc.strerror), file=sys.stderr)
        print(
            "mugit version %s (python %d.%d%s)"
            % (
                mugit.version,
                sys.version_info.major,
                sys.version_info.minor,
                gitVersion or ""
            )
        )
        return 0
    if len(unknownOptions) > 0:
        for option in unknownOptions:
            print("error: unknown option: %s" % (option))
        print("")
        PrintUsage()
        return 1
    if commandName is None:
        print("error: no command given")
        print("")
        PrintUsage()
        return 1
    try:
        if not os.path.isdir(".git"):
            raise Exception("not in a git workspace")
        command = mugit.commands[commandName]()
        return command(commandArgs)
    except KeyError:
        print("error: no such command: %s" % (commandName))
        print("")
        PrintUsage()
        return 1
    except Exception as exc:
        print("error: %s" % (str(exc)), file=sys.stderr)
        return 1
    return 0

def MainEntry():
    return Main(sys.argv)
