from ..commands.command import Command

class Cog:
    def __init__(self, bot):
        self.bot = bot
        self.commands = []

    def add_command(self, **kwargs):
        description = kwargs.get("description", "")
        usage = kwargs.get("usage", "")
        aliases = kwargs.get("aliases", [])
        name = kwargs.get("name", "None")
        callback = kwargs.get("callback")
        registered_with_function = kwargs.get("registered_with_function", True)

        self.bot.register_command(**kwargs)
        self.commands.append(Command(name, description, usage, aliases, callback, registered_with_function=registered_with_function))

    def command(self, **kwargs):
        def decorator(func):
            self.add_command(**kwargs, callback=func)
            return func
        return decorator