import requests
import socketio
import asyncio
import importlib
import traceback
import base64
import os
import shlex
import datetime
import inspect

from .command import Command
from .events import Events

from ..extra import Extra
from ..user import User
from ..message import Message
from .. import nertivia

class Client:
    def __init__(self, command_prefix, debug=False):
        self.token = ""
        self.socket = socketio.Client(engineio_logger=False, logger=debug)
        self.socketIp = "https://nertivia.net/"
        self.headers = {"Authorization": self.token, "content-type": "application/json"}
        self.user = ""
        self.start_time = datetime.datetime.now()
        self.command_prefix = command_prefix
        self.commands = []

        Extra.setauthtoken(self.token)    

    def run(self, token):
        self.token = token
        # self.user = User(response.json()["user"]["id"], response.json()["user"]["username"], response.json()["user"]["tag"], response.json()["user"]["avatar"], response.json()["user"]["banner"], response.json()["user"]["created"])
        self.user = nertivia.Nertivia(token)
        Extra.setauthtoken(token)
        self.socket.connect(self.socketIp, namespaces=["/"], transports=["websocket"])
        self.socket.emit("authentication", {"token": token})
        self.socket.wait()
        self.start_time = datetime.datetime.now()

    def parse_message(self, message):
        command = message.content.replace(self.command_prefix, "")
        args = shlex.split(command)
        command = args[0]
        args.pop(0)

        return command, args

    def _command_event_handler(self, event):
        message = Message(event["message"]["messageID"], event["message"]["channelId"])

        if message.content.startswith(self.command_prefix):
            cmd, args = self.parse_message(message)
            for command in self.commands:
                if command.name == cmd:
                    callback = command.get_callback()
                    callback(message, args)

    def register_command(self, name: str, callback: callable):
        self.commands.append(Command(name, callback))

        self.socket.on("message:created", self._command_event_handler)

    def event(self, *args):
        eventname = args[0].__name__

        events = Events().events

        for event in events:
            for key, value in event.items():
                if key == eventname:
                    self.socket.on(value, args[0])
        