import requests
import ast
import socketio

from .channel import Channel
from .server import Server
from .user import User
from .bot import Bot
from .extra import Extra
from . import gateway

class Nertivia:
    def __init__(self, token) -> None: 
        global __token
        response = requests.get("https://nertivia.net/api/user", headers={"Authorization": token})
        self.token = token
        self.id = response.json()["user"]["id"]
        self.avatar = response.json()["user"]["avatar"]
        self.banner = response.json()["user"]["banner"]
        self.username = response.json()["user"]["username"]
        self.tag = response.json()["user"]["tag"]
        self.created = response.json()["user"]["created"]
        self.mention = f"[@:{self.id}]"

        self.servers = []

        Extra.setauthtoken(self.token)

    def get_server(self, id) -> Server:
        return Server(id)

    def get_channel(self, id) -> Channel:
        return Channel(id)

    def get_user(self, id) -> User:
        return User(id)

    def create_channel(self, server_id, name):
        response = requests.put(
            f"https://nertivia.net/api/servers/{server_id}/channels",
            headers={"Authorization": self.token, "content-type": "application/json"},
            json={"name": name}
        )

        return response.json()

    def set_status(self, status):
        response = requests.post(
            "https://nertivia.net/api/settings/status",
            headers={"Authorization": self.token, "content-type": "application/json"},
            json={"status": status}
        )

        return response.json()

    def set_custom_status(self, text):
        response = requests.post(
            "https://nertivia.net/api/settings/custom-status",
            headers={"Authorization": self.token, "content-type": "application/json"},
            json={"custom_status": text}
        )

        return response.json()

    def _get_servers_handler(self, event):
        data = ast.literal_eval(str(event))
        self.servers = data["user"]["servers"]

    def get_servers(self) -> list:
        socket = socketio.Client()
        socket.connect("https://nertivia.net/", namespaces=["/"], transports=["websocket"])
        socket.emit("authentication", {"token": Extra.getauthtoken()})

        socket.on(gateway.events.Events().get_event("on_success"), self._get_servers_handler)

        while len(self.servers) == 0:
            pass

        socket.disconnect()

        return self.servers

    def get_bots(self) -> list:
        response = requests.get(
            "https://nertivia.net/api/bots",
            headers={"Authorization": self.token}
        )

        bots = []

        for bot in response.json():
            bot2 = Bot(bot["id"])
            bots.append(bot2)

        return bots

    def create_bot(self) -> Bot:
        response = requests.post(
            "https://nertivia.net/api/bots",
            headers={"Authorization": self.token, "content-type": "application/json"}
        )

        return Bot(response.json()["id"])

    def get_bot(self, id) -> Bot:
        response = requests.get(
            "https://nertivia.net/api/bots/" + str(id),
            headers={"Authorization": self.token}
        )

        bot = Bot(response.json()["id"], response.json()["username"], response.json()["tag"], response.json()["avatar"], response.json()["botCommands"])
        return bot

    def delete_bot(self, id):
        response = requests.delete(
            "https://nertivia.net/api/bots/" + str(id),
            headers={"Authorization": self.token}
        )

        return response.json()

    