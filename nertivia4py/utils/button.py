class Button:
    """
    Nertivia Button

    Attributes:
        name (str): The name of the button.
        id (int): The id of the button.
    """

    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.json = {
            "name": name,
            "id": id
        }

    def __str__(self) -> str:
        return f"{self.name}:{self.id}"