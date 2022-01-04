import requests

from . import embed
from . import user
from . import extra
from . import channel
from . import dmchannel

class Message:
    def __init__(self, id, channelId, creator="", content="", created=""):
        if creator == "" or content == "" or created == "":
            response = requests.get(
                f"https://nertivia.net/api/messages/{id}/channels/{channelId}",
                headers={"authorization": extra.Extra.getauthtoken()}
            )

            channelResponse = requests.get(
                f"https://nertivia.net/api/channels/{response.json()['channelID']}",
                headers={"authorization": extra.Extra.getauthtoken()}
            )

            if "recipients" in channelResponse.json():
                self.channel = dmchannel.DMChannel(response.json()["channelID"])
            else:
                self.channel = channel.Channel(response.json()["channelID"])

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
            self.channel = channel.Channel(channelId)
            self.content = content
            self.created = created
            self.creator = creator

    def __str__(self):
        return self.content

    def reply(self, content:str = "", embed: embed.Embed = None, buttons: list = None):
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

    def edit(self, content, embed: embed.Embed = None, buttons: list = None):
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

    def delete(self):
        response = requests.delete(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def addReaction(self, emoji):
        response = requests.post(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}/reactions",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={"unicode": emoji, "gif": False}
        )

        return response.json()

    def removeReaction(self, emoji):
        response = requests.delete(
            f"https://nertivia.net/api/messages/{self.id}/channels/{self.channel.id}/reactions",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={"unicode": emoji}
        )

        return response.json()