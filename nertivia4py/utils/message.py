import requests

from . import embed
from . import user
from . import extra
from . import textchannel
from . import dmchannel

class Message:
    """
Nertivia Message

Attributes:
- id (int): The ID of the message.
- channel (textchannel.TextChannel): The channel the message was sent in.
- creator (user.User): The author of the message.
- content (str): The content of the message.
- created (str): The time the message was created.
    """

    def __init__(self, id, channelId, creator="", content="", created="") -> None:
        if creator == "" or content == "" or created == "":
            response = requests.get(
                f"https://nertivia.net/api/messages/{id}/channels/{channelId}",
                headers={"authorization": extra.Extra.getauthtoken()}
            )

            channel_response = requests.get(
                f"https://nertivia.net/api/channels/{response.json()['channelId']}",
                headers={"authorization": extra.Extra.getauthtoken()}
            )

            if "recipients" in channel_response.json():
                self.channel = dmchannel.DMChannel(response.json()["channelId"])
            else:
                self.channel = textchannel.TextChannel(response.json()["channelId"])

            self.id = response.json()["messageID"]
            # check if response json has a key called message and if it does then set self.content to that value
            try:
                self.content = response.json()["message"]
            except:
                self.content = ""
            try:
                self.created = response.json()["created"]
            except:
                self.created = ""
            try:
                self.creator = user.User(response.json()["creator"]["id"])
            except:
                self.creator = None

        else:
            self.id = id
            self.channel = textchannel.TextChannel(channelId)
            self.content = content
            self.created = created
            self.creator = creator

    def __str__(self) -> str:
        return self.content

    def reply(self, content:str = "", embed: embed.Embed = None, buttons: list = None) -> "Message":
        """
Replies to the message.

Args:
- content (str): The content of the message.
- embed (embed.Embed): The embed of the message.
- buttons (list of button.Button): A list of buttons to add to the message.

Returns:
- Message: The message that was sent.
        """

        body={"message": f"<m{self.id}>"+content}
        if embed != None:
            body["htmlEmbed"] = embed.json
        if buttons != None:
            body["buttons"] = []
            for button in buttons:
                body["buttons"].append(button.json)

        response = requests.post(
            f"https://nertivia.net/api/messages/channels/{self.channel.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json=body
        )

        return Message(response.json()["messageCreated"]["messageID"], self.channel.id)

    def edit(self, content, embed: embed.Embed = None, buttons: list = None) -> dict:
        """
Edits the message.

Args:
- content (str): The content of the message.
- embed (embed.Embed): The embed of the message.
- buttons (list of button.Button): A list of buttons to add to the message.

Returns:
- dict: The response of the request.
        """

        content = str(content)
        body = {"message": content}
        if embed is not None:
            body["htmlEmbed"] = embed.json
        if buttons is not None:
            body["buttons"] = []
            for button in buttons:
                body["buttons"].append(button.json)

        response = requests.patch(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json=body
        )

        return response.json()

    def delete(self) -> dict:
        """
Deletes the message.
    
Returns:
- dict: The response of the request.
        """

        response = requests.delete(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def add_reaction(self, emoji) -> dict:
        """
Adds a reaction to the message.

Args:
- emoji (str): The emoji to add.

Returns:
- dict: The response of the request.
        """

        response = requests.post(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}/reactions",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={"unicode": emoji, "gif": False}
        )

        return response.json()

    def remove_reaction(self, emoji) -> dict:
        """
Removes a reaction to the message.

Args:
- emoji (str): The emoji to remove.

Returns:
- dict: The response of the request.
        """

        response = requests.delete(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}/reactions",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={"unicode": emoji}
        )

        return response.json()