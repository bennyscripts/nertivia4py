import requests
import datetime
import socketio
import ast
import json

from nertivia4py.gateway import events
from . import textchannel
from . import user
from . import extra

class Server:
    """
    Nertivia Server

    Attributes:
    - id (str): The server's ID.
    - name (str): The server's name.
    - avatar (str): The server's avatar.
    - default_channel_id (str): The server's default channel ID.
    - created (str): The server's creation date.
    - banner (str): The server's banner.
    """

    def __init__(self, id, name="", avatar="", default_channel_id="", created="", banner="") -> None:
        if name == "" or avatar == "" or default_channel_id == "" or created == "" or banner == "":
            response = requests.get(
                f"https://nertivia.net/api/servers/{id}",
                headers={"authorization": extra.Extra.getauthtoken()}
            )

            self.id = response.json()["server_id"]
            self.name = response.json()["name"]
            self.avatar = response.json()["avatar"]
            self.default_channel_id = response.json()["default_channel_id"]
            self.created = response.json()["created"]
            self.created_at = datetime.datetime.fromtimestamp(int(self.created) / 1000)

        else:
            self.id = id
            self.name = name
            self.avatar = avatar
            self.default_channel_id = default_channel_id
            self.created = created
            self.created_at = datetime.datetime.fromtimestamp(int(self.created) / 1000)
            # self.banner = banner

        self.members = []
        self.channels = []

    def __str__(self):
        return f"{self.name}"

    def edit(self, name) -> dict:
        """
        Edits the server

        Args:
        - name (str): The new name of the server.

        Returns:
        - dict: The response of the request.
        """

        response = requests.patch(
            f"https://nertivia.net/api/servers/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={
                "name": name
            }
        )

        self.name = response.json()["name"]
        return response.json()

    def delete(self) -> dict:
        """
        Deletes the server

        Returns:
        - dict: The response of the request.
        """

        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def get_bans(self):
        """
        Gets a list of banned users from the server

        Returns:
        - list: A list of banned users.
        - None: If the request failed.
        """

        response = requests.get(
            f"https://nertivia.net/api/servers/{self.id}/bans",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            bans = []

            for user3 in response.json():
                user4 = user3["user"]
                user2 = user.User(user["id"])
                bans.append(user2)

            return bans
        
        else:
            return False

    def ban_member(self, user: user.User) -> bool:
        """
        Bans a member from the server

        Args:
        - user (user.User): The user to ban.

        Returns:
        - bool: Whether the request was successful.
        """

        userId = user.id
        response = requests.put(
            f"https://nertivia.net/api/servers/{self.id}/bans/{userId}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            return True
        else:
            return False

    def kick_member(self, user: user.User) -> bool:
        """
        Kicks a member from the server

        Args:
        - user (user.User): The user to kick.

        Returns:
        - bool: Whether the request was successful.
        """

        userId = user.id
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}/members/{userId}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            return True
        else:
            return False

    def unban_member(self, user: user.User) -> dict:
        """
        Unbans a member from the server

        Args:
        - user (user.User): The user to unban.

        Returns:
        - dict: The response of the request.
        """

        userId = user.id
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}/bans/{userId}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def _get_members_handler(self, event):
        data = ast.literal_eval(str(event))

        members = []
        for servermember in data["serverMembers"]:
            if servermember["server_id"] == str(self.id):
                members.append(servermember)

        self.members = members

    def get_members(self) -> list:
        """
        Gets a list of members from the server

        Aliases:
        - get_all_members()

        Returns:
        - list: A list of members.
        """

        socket = socketio.Client()
        socket.connect("https://nertivia.net/", namespaces=["/"], transports=["websocket"])
        socket.emit("authentication", {"token": extra.Extra.getauthtoken()})

        socket.on(events.Events().get_event("on_success"), self._get_members_handler)

        while len(self.members) == 0:
            pass

        socket.disconnect()

        return self.members

    def _get_channels_handler(self, event):
        data = ast.literal_eval(str(event))
        servers = data["user"]["servers"]
        channels = []

        for server in servers:
            if server["server_id"] == self.id:
                for chnl in server["channels"]:
                    chnl2 = textchannel.TextChannel(chnl["channelID"], chnl["name"], chnl["server_id"])
                    channels.append(chnl2)

        self.channels = channels

    def get_channels(self) -> list:
        """
        Gets a list of channels from the server

        Aliases:
        - get_all_channels()

        Returns:
        - list: A list of channels.
        """

        socket = socketio.Client()
        socket.connect("https://nertivia.net/", namespaces=["/"], transports=["websocket"])
        socket.emit("authentication", {"token": extra.Extra.getauthtoken()})

        socket.on(events.Events().get_event("on_success"), self._get_channels_handler)

        while len(self.channels) == 0:
            pass

        socket.disconnect()

        return self.channels

    def create_text_channel(self, name):
        """
        Creates a text channel in the server.

        Args:
        - name (str): The name of the channel.

        Returns:
        - textchannel.TextChannel: The channel that was created.
        """

        response = requests.put(
            f"https://nertivia.net/api/servers/{self.id}/channels",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={
                "name": name,
                "type": 1
            }
        )

        return textchannel.TextChannel(response.json()["channel"]["channelId"])

    get_all_members = get_members
    get_all_channels = get_channels