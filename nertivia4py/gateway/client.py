import socketio
import shlex

from . import events
from . import command

from .. import nertivia
from .. import extra
from .. import message

class Client:
    def __init__(self, command_prefix, debug=False) -> None:
        self.socket = socketio.Client(engineio_logger=False, logger=debug)
        self.socket_ip = "https://nertivia.net/"

        self.command_prefix = command_prefix
        self.commands = []

        self.user = None
        self.token = ""

        extra.Extra.setauthtoken(self.token)

    def run(self, token) -> None:
        extra.Extra.setauthtoken(token)

        self.token = token
        self.user = nertivia.Nertivia(token)

        self.socket.connect(self.socket_ip, namespaces=["/"], transports=["websocket"])
        self.socket.emit("authentication", {"token": token})
        self.socket.wait()

    def _command_event_handler(self, event):
        msg = message.Message(event["message"]["messageID"], event["message"]["channelId"])

        if msg.content.startswith(self.command_prefix):
            command = msg.content.replace(self.command_prefix, "")
            args = shlex.split(command)
            command = args[0]
            args.pop(0)

            for cmd in self.commands:
                if cmd.name == command or command in cmd.aliases:
                    callback = cmd.get_callback()
                    callback(msg, args)

    def event(self, *args):
        eventname = args[0].__name__

        evnts = events.Events().events

        for event in evnts:
            for key, value in event.items():
                if key == eventname:
                    self.socket.on(value, args[0])

    def command(self, **kwargs):
        def decorator(func):
            command_name = kwargs["name"] if "name" in kwargs else func.__name__
            command_description = kwargs["description"] if "description" in kwargs else "No description provided."
            command_usage = kwargs["usage"] if "usage" in kwargs else ""
            command_aliases = kwargs["aliases"] if "aliases" in kwargs else []

            command_callback = func

            self.commands.append(command.Command(command_name, command_description, command_usage, command_aliases, command_callback))
            self.socket.on(events.Events().get_event("on_message"), self._command_event_handler)

            return func
        return decorator