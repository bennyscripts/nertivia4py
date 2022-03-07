import requests

from . import extra
from . import user

class Bot:
    """
Nertivia Bot User

Attributes:
- id (int): The ID of the bot.
- username (str): The username of the bot.
- tag (str): The tag of the bot.
- avatar (str): The avatar of the bot.
- commands (list): The commands of the bot.
- creator (user.User): The creator of the bot.
    """

    def __init__(self, id, username="", tag="", avatar="", commands=[], creator = None) -> None:
        if username == "" or tag == "" or avatar == "" or commands == [] or creator is None:
            response = requests.get(
                f"https://nertivia.net/api/bots/{id}",
                headers={"Authorization": extra.Extra.getauthtoken()}
            )
            
            self.id = response.json()["id"]
            self.username = response.json()["username"]
            self.tag = response.json()["tag"]
            self.avatar = response.json()["avatar"]
            self.commands = response.json()["botCommands"]
            self.creator = user.User(response.json()["createdBy"]["id"])

        else:
            self.id = id
            self.username = username
            self.tag = tag
            self.avatar = avatar
            self.commands = commands
            self.creator = creator

    def __str__(self):
        return f"{self.username}:{self.tag}"

    def delete(self) -> dict:
        """
Deletes the bot.

Returns:
    dict: The response of the request.
        """

        response = requests.delete(
            "https://nertivia.net/api/bots/" + str(self.id),
            headers={"Authorization": self.token}
        )

        return response.json()