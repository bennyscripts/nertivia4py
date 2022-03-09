import inspect

class Command:
    def __init__(self, name: str, description: str, usage: str, aliases: list, callback: callable = None, registered_with_function: bool = True) -> None:
        self.name = name
        self.description = description
        self.aliases = aliases
        self.usage = usage
        self.callback = callback
        self.registered_with_function = registered_with_function

        self.cog = None
        if "self" in self.callback.__code__.co_varnames:
            self.cog = self.callback.__code__.co_varnames[0]

    def get_callback(self) -> callable:
        return self.callback