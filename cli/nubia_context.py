#!/usr/bin/env python3

from nubia import context, eventbus, exceptions


class NubiaNgxStatsContext(context.Context):
    def __init__(self):
        self.verbose = False
        super().__init__()

    def on_connected(self, *args, **kwargs):
        pass

    async def on_cli(self, cmd, args):
        # dispatch the on connected message
        self.verbose = args.verbose
        await self.registry.dispatch_message(eventbus.Message.CONNECTED)

    async def on_interactive(self, args):
        self.verbose = args.verbose
        ret = await self._registry.find_command("connect").run_cli(args)
        if ret:
            raise exceptions.CommandError("Failed starting interactive mode")
        # dispatch the on connected message
        await self.registry.dispatch_message(eventbus.Message.CONNECTED)
