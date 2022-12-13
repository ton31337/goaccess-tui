#!/usr/bin/env python3

import sys

from nubia_plugin import NubiaNgxStatsPlugin

import commands
from nubia import Nubia, Options

if __name__ == "__main__":
    plugin = NubiaNgxStatsPlugin()
    shell = Nubia(
        name="ngx-stats",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(
            persistent_history=False, auto_execute_single_suggestions=False
        ),
    )
    sys.exit(shell.run())
