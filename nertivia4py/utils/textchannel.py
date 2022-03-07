import requests

from . import message
from . import extra
from . import embed
from . import user
from . import server

class TextChannel:
    """
    Nertivia Text Channel

    Attributes:
    - id (int): The ID of the channel.
    - name (str): The name of the channel.
    - server_id (int): The ID of the server.
    """

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
        """
        Sends a message to the channel.

        Args:
        - content (str): The content of the message.
        - embed (embed.Embed): The embed of the message.
        - buttons (list): A list of buttons to add to the message.

        Aliases:
        - send_message(content, embed, buttons)

        Returns:
        - message.Message: The message that was sent.
        """

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

    def edit(self, name) -> dict:
        """
        Edits the channel

        Args:
        - name (str): The new name of the channel.

        Returns:
        - dict: The response of the request.
        """

        response = requests.patch(
            f"https://nertivia.net/api/servers/{self.server_id}/channels/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={
                "name": name
            }
        )

        self.name = name

        return response.json()

    def delete(self) -> dict:
        """
        Deletes the channel.

        Returns:
        - dict: The response of the request.
        """

        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.server_id}/channels/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def typing(self):
        """
        Tells the channel that the user is typing.

        Returns:
        - requests response: The response of the request.
        """

        response = requests.post(
            f"https://nertivia.net/api/messages/{self.id}/typing",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response

    def get_messages(self, amount: int = 1) -> list:
        """
        Gets the messages from the channel.

        Args:
        - amount (int): The amount of messages to get.

        Returns:
        - list: The messages.
        """

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
        """
        Gets a message from the channel.

        Args:
        - id (int): The ID of the message.

        Returns:
        - message.Message: The message.
        - None: If the message doesn't exist.
        """

        messages = self.getMessages()
        for message in messages:
            if message.id == id:
                return message
        
        return None

    send_message = send