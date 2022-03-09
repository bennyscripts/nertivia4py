from ..commands.command import Command

class Cog:
    def __init__(self, bot):
        self.bot = bot
        self.commands = []

    def add_command(self, **kwargs):
        description = kwargs["description"] if "description" in kwargs else ""
        usage = kwargs["usage"] if "usage" in kwargs else ""
        aliases = kwargs["aliases"] if "aliases" in kwargs else []
        name = kwargs["name"] if "name" in kwargs else "None"
        callback = kwargs["callback"] if "callback" in kwargs else None
        registered_with_function = kwargs["registered_with_function"] if "registered_with_function" in kwargs else True

        self.bot.register_command(**kwargs)
        self.commands.append(Command(name, description, usage, aliases, callback, registered_with_function=registered_with_function))

    def command(self, **kwargs):
        def decorator(func):
            self.add_command(**kwargs, callback=func)
            return func
        return decorator