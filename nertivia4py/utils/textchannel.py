import requests

from . import message
from . import extra
from . import embed
from . import user
from . import server

class TextChannel:
    def __init__(self, id, name="", server_id="") -> None:
        if name == "" or server_id == "":
            response = requests.get(f"https://nertivia.net/api/channels/{id}", headers={"authorization": extra.Extra.getauthtoken()})

            self.id = response.json()["channelId"]
            self.name = response.json()["name"]
            self.server = server.Server(response.json()["server_id"])
        
        else:
            self.id = id
            self.name = name
            self.server = server.Server(server_id)

    def __str__(self) -> str:
        return self.name

    def send(self, content = "", embed: embed.Embed = None, buttons: list = None) -> message.Message:
        content = str(content)
        body={}

        if content != "":
            body["message"] = content

        if embed != None:
            body["htmlEmbed"] = embed.json

        if buttons != None:
            body["buttons"] = []
            for button in buttons:
                body["buttons"].append(button.json)

        response = requests.post(
            f"https://nertivia.net/api/messages/channels/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json=body
        )

        if "messagecreated" not in response.text.lower():
            return False

        return message.Message(response.json()["messageCreated"]["messageID"], self.id)

    def edit(self, name):
        response = requests.patch(
            f"https://nertivia.net/api/servers/{self.server_id}/channels/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={
                "name": name
            }
        )

        self.name = name

        return response.json()

    def delete(self):
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.server_id}/channels/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def typing(self):
        response = requests.post(
            f"https://nertivia.net/api/messages/{self.id}/typing",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response

    def get_messages(self, amount: int = 1) -> list:
        messages = []
        index = 0
        response = requests.get(
            f"https://nertivia.net/api/messages/channels/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        for item in response.json()["messages"]:
            index += 1
            try:
                author = user.User(item["creator"]["id"], item["creator"]["username"], item["creator"]["tag"], item["creator"]["avatar"])
                message = message.Message(item["messageID"], self.id, author, item["message"], item["created"])
                messages.append(message)
            except:
                pass

            if index == amount:
                break
        
        return messages

    def get_message(self, id):
        messages = self.getMessages()
        for message in messages:
            if message.id == id:
                return message
        
        return None

    send_message = send