import requests

from . import embed
from . import extra

class DMChannel:
    """
    Nertivia DM Channel
    Same as Text Channel but is used to send messages to a user.

    Attributes:
        id (int): The ID of the channel.
    """

    def __init__(self, id) -> None: 
        self.id = id

    def send(self, content = "", embed: embed.Embed = None, buttons: list = None) -> dict:
        """
        Sends a message to the channel.

        Args:
            content (str): The content of the message.
            embed (embed.Embed): The embed of the message.
            buttons (list): The buttons of the message.

        Aliases:
            send_message(content, embed, buttons)
            
        Returns:
            dict: The response of the request.
        """

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

        response = requests.post(f"https://nertivia.net/api/messages/channels/{self.id}", headers={"authorization": extra.Extra.getauthtoken()}, json=body)
        return response.json()

    send_message = send