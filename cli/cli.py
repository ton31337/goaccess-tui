#!/usr/bin/env python3

import sys

from nubia_plugin import NubiaGoAccessPlugin

import commands
from nubia import Nubia, Options

if __name__ == "__main__":
    plugin = NubiaGoAccessPlugin()
    shell = Nubia(
        name="goaccess",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(
            persistent_history=True, auto_execute_single_suggestions=False
        ),
    )
    sys.exit(shell.run())
