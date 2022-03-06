class Command:
    def __init__(self, name: str, description: str, usage: str, aliases: list, callback: callable) -> None:
        self.name = name
        self.description = description
        self.aliases = aliases
        self.usage = usage
        self.callback = callback

    def get_callback(self) -> callable:
        return self.callback