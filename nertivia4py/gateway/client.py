import requests
import socketio
import asyncio
import importlib
import traceback
import base64
import os
import shlex
import datetime

from .events import Events

from ..extra import Extra
from ..user import User
from ..message import Message
from .. import nertivia

class Client:
    def __init__(self, command_prefix, commands_path="", debug=False):
        self.token = ""
        self.socket = socketio.Client(engineio_logger=False, logger=debug)
        self.socketIp = "https://nertivia.net/"
        self.headers = {"Authorization": self.token, "content-type": "application/json"}
        self.user = ""
        self.start_time = datetime.datetime.now()
        self.command_paths = commands_path
        self.command_prefix = command_prefix
        self.commands = []

        if self.command_paths != "":
            for file in os.listdir(self.command_paths):
                if file.endswith(".py"):
                    if file.replace(".py", "") in self.commands:
                        continue

                    if self.checkIfCommand(file.replace(".py", "")):
                        self.commands.append(self.getCommand(file.replace(".py", "")))

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

    def parseMessage(self, message):
        command = message.content.replace(self.command_prefix, "")
        args = shlex.split(command)
        command = args[0]
        args.pop(0)

        return command, args

    def executeCommand(self, path, context, args):
        paths = path.split(".")

        commandmodule = importlib.import_module(path)
        moduleName = commandmodule.__name__.removeprefix(paths[0] + ".")
        moduleName = moduleName[0].upper() + moduleName[1:]
        
        class_ = getattr(commandmodule, moduleName)
        instance = class_(self)
        instance.command(context, args)

    def checkIfCommand(self, command):
        if not os.path.exists(self.command_paths + "/" + command + ".py"): 
            return False

        commandmodule = importlib.import_module(self.command_paths + "." + command)
        moduleName = commandmodule.__name__.removeprefix(self.command_paths + ".")
        moduleName = moduleName[0].upper() + moduleName[1:]

        class_ = getattr(commandmodule, moduleName)
        instance = class_(self)
        func = getattr(instance, "command")

        if callable(func):
            return True

        return False

    def getCommand(self, command):
        commandmodule = importlib.import_module(self.command_paths + "." + command)
        moduleName = commandmodule.__name__.removeprefix(self.command_paths + ".")
        moduleName = moduleName[0].upper() + moduleName[1:]

        class_ = getattr(commandmodule, moduleName)
        instance = class_(self)

        return instance

    def event(self, *args):
        eventname = args[0].__name__

        events = Events().events

        for event in events:
            for key, value in event.items():
                if key == eventname:
                    self.socket.on(value, args[0])