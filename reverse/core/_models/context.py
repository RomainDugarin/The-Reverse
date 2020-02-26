from discord.ext.commands import Context

class Context(Context):

    def __init__(self, ctx: Context):
        super().__init__(
            message=ctx.message,
            bot=ctx.bot,
            args=ctx.args,
            kwargs=ctx.kwargs,
            prefix=ctx.prefix,
            command=ctx.command,
            view=ctx.view,
            invoked_with=ctx.invoked_with,
            invoked_subcommand=ctx.invoked_subcommand,
            subcommand_passed=ctx.subcommand_passed,
            command_failed=ctx.command_failed,
            _state=ctx._state
        )
        self.run()
    
    def run(self):
        self.on_message()
    
    def on_message(self):
        print('New context found, can be stored')

    def getData(self):
        return self.data
    
