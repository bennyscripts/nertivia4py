import requests
import datetime
import socketio
import ast
import json

from . import gateway
from . import channel
from .user import User
from .extra import Extra

class Server:
    def __init__(self, id, name="", avatar="", defaultChannelId="", created="", banner=""):
        if name == "" or avatar == "" or defaultChannelId == "" or created == "" or banner == "":
            response = requests.get(
                f"https://nertivia.net/api/servers/{id}",
                headers={"authorization": Extra.getauthtoken()}
            )

            self.id = response.json()["server_id"]
            self.name = response.json()["name"]
            self.avatar = response.json()["avatar"]
            self.defaultChannel = channel.Channel(response.json()["default_channel_id"])
            self.created = response.json()["created"]
            self.created_at = datetime.datetime.fromtimestamp(int(self.created) / 1000)
            # self.banner = response.json()["banner"]

        else:
            self.id = id
            self.name = name
            self.avatar = avatar
            self.defaultChannel = channel.Channel(defaultChannelId)
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
            headers={"authorization": Extra.getauthtoken()},
            json={
                "name": name
            }
        )

        self.name = response.json()["name"]
        return response.json()

    def delete(self):
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}",
            headers={"authorization": Extra.getauthtoken()}
        )

        return response.json()

    def getBans(self):
        response = requests.get(
            f"https://nertivia.net/api/servers/{self.id}/bans",
            headers={"authorization": Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            bans = []

            for user in response.json():
                user = user["user"]
                user2 = User(user["id"])
                bans.append(user2)

            return bans
        
        else:
            return False

    def banMember(self, user: User):
        userId = user.id
        response = requests.put(
            f"https://nertivia.net/api/servers/{self.id}/bans/{userId}",
            headers={"authorization": Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            return True
        else:
            return False

    def kickMember(self, user: User):
        userId = user.id
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}/members/{userId}",
            headers={"authorization": Extra.getauthtoken()}
        )

        if "missing permission" not in response.text.lower():
            return True
        else:
            return False

    def unbanMember(self, user: User):
        userId = user.id
        response = requests.delete(
            f"https://nertivia.net/api/servers/{self.id}/bans/{userId}",
            headers={"authorization": Extra.getauthtoken()}
        )

        return response.json()

    def getMembersHandler(self, event):
        data = ast.literal_eval(str(event))

        members = []
        for servermember in data["serverMembers"]:
            if servermember["server_id"] == str(self.id):
                members.append(servermember)

        self.members = members

    def getMembers(self):
        socket = socketio.Client()
        socket.connect("https://nertivia.net/", namespaces=["/"], transports=["websocket"])
        socket.emit("authentication", {"token": Extra.getauthtoken()})

        socket.on(gateway.events.Events().get_event("on_success"), self.getMembersHandler)

        while len(self.members) == 0:
            pass

        socket.disconnect()

        return self.members

    def getChannelsHandler(self, event):
        data = ast.literal_eval(str(event))
        servers = data["user"]["servers"]
        channels = []

        for server in servers:
            if server["server_id"] == self.id:
                for chnl in server["channels"]:
                    chnl2 = channel.Channel(chnl["channelID"], chnl["name"], chnl["server_id"])
                    channels.append(chnl2)

        self.channels = channels

    def getChannels(self):
        socket = socketio.Client()
        socket.connect("https://nertivia.net/", namespaces=["/"], transports=["websocket"])
        socket.emit("authentication", {"token": Extra.getauthtoken()})

        socket.on(gateway.events.Events().get_event("on_success"), self.getChannelsHandler)

        while len(self.channels) == 0:
            pass

        socket.disconnect()

        return self.channels