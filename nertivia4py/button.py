class Button:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.json = {
            "name": name,
            "id": id
        }

    def __str__(self):
        return f"{self.name}:{self.id}"