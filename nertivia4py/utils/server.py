import requests
import datetime
import socketio
import ast
import json

from nertivia4py.gateway import events
from . import channel
from . import user
from . import extra

class Server:
    def __init__(self, id, name="", avatar="", default_channel_id="", created="", banner="") -> None:
        if name == "" or avatar == "" or default_channel_id == "" or created == "" or banner == "":
            response = requests.get(
                f"https://nertivia.net/api/servers/{id}",
                headers={"authorization": extra.Extra.getauthtoken()}
            )

            self.id = response.json()["server_id"]
            self.name = response.json()["name"]
            self.avatar = response.json()["avatar"]
            self.default_channel = channel.Channel(response.json()["default_channel_id"])
            self.created = response.json()["created"]
            self.created_at = datetime.datetime.fromtimestamp(int(self.created) / 1000)
            # self.banner = response.json()["banner"]

        else:
            self.id = id
            self.name = name
            self.avatar = avatar
            self.default_channel = channel.Channel(default_channel_id)
            self.created = created
            self.created_at = datetime.datetime.fromtimestamp(int(self.created) / 1000)
            # self.banner = banner

        self.members = []
        self.channels = []

    def __str__(self):
        return f"{self.name}"

    def edit(self, name):
        response = requests.patch(
            f"https://nertivia.net/api/servers/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()},
            json={
                "name": name
            }
        )

        self.name = response.json()["name"]
        return response.json()

    def delete(self):
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        return response.json()

    def get_bans(self):
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
        userId = user.id
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}/members/{userId}",
            headers={"authorization": extra.Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            return True
        else:
            return False

    def unban_member(self, user: user.User):
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
                    chnl2 = channel.Channel(chnl["channelID"], chnl["name"], chnl["server_id"])
                    channels.append(chnl2)

        self.channels = channels

    def get_channels(self) -> list:
        socket = socketio.Client()
        socket.connect("https://nertivia.net/", namespaces=["/"], transports=["websocket"])
        socket.emit("authentication", {"token": extra.Extra.getauthtoken()})

        socket.on(events.Events().get_event("on_success"), self._get_channels_handler)

        while len(self.channels) == 0:
            pass

        socket.disconnect()

        return self.channels

    get_all_members = get_members
    get_all_channels = get_channels