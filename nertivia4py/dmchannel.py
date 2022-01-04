import requests

from .embed import Embed
from .extra import Extra

class DMChannel:
    def __init__(self, id): 
        self.id = id

    def send(self, content = "", embed: Embed = None, buttons: list = None):
        content = str(content)
        body = {}
        if content != "":
            body["message"] = content
        if embed is not None:
            body["htmlEmbed"] = embed.json
        if buttons != None:
            body["buttons"] = []
            for button in buttons:
                body["buttons"].append(button.json)

        response = requests.post(
            f"https://nertivia.net/api/messages/channels/{self.id}",
            headers={"authorization": Extra.getauthtoken()},
            json=body
        )

        return response.json()