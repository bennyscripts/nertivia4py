class Command:
    def __init__(self, name: str, callback: callable) -> None:
        self.name = name
        self.callback = callback

    def get_callback(self) -> callable:
        return self.callback