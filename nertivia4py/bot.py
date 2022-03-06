import socketio
import shlex
import requests
import importlib

from .gateway import events
from .commands import command

from .utils import user
from .utils import extra
from .utils import message
from .utils import exceptions

class Bot:
    """
    Nertivia Gateway Client  
    This is the client that handles all of the events from the Nertivia Gateway.  
    And it also handles all of the commands that are sent to the bot.  

    Attributes:
        command_prefix (str): The prefix that is used to identify commands.
        self_bot (bool): Whether or not the bot is a self bot.
        debug (bool): Whether or not to send socket debug messages.
    """

    def __init__(self, command_prefix, self_bot=False, debug=False) -> None:
        self.socket = socketio.Client(engineio_logger=False, logger=debug)
        self.socket_ip = "https://nertivia.net/"

        self.command_prefix = command_prefix
        self.commands = []

        self.user = None
        self.token = ""
        self.self_bot = self_bot

        extra.Extra.setauthtoken(self.token)

    def run(self, token) -> None:
        """
        Run the client  

        Args:
            token (str): The token that is used to authenticate the bot.

        Raises:
            InvalidToken: If the token is invalid.
        """

        extra.Extra.setauthtoken(token)

        self.token = token

        user_response = requests.get("https://nertivia.net/api/user", headers={"authorization": extra.Extra.getauthtoken()})
        if user_response.status_code != 200:
            raise exceptions.InvalidToken("Token is invalid.")

        user_obj = user_response.json()["user"]

        self.user = user.User(user_obj["id"])

        self.socket.connect(self.socket_ip, namespaces=["/"], transports=["websocket"])
        self.socket.emit("authentication", {"token": token})
        self.socket.wait()

    def _command_event_handler(self, event):
        msg = message.Message(event["message"]["messageID"], event["message"]["channelId"])
        command_can_be_run = False

        if self.self_bot:
            if msg.creator.id == self.user.id:
                command_can_be_run = True
        else:
            if msg.creator.id != self.user.id:
                command_can_be_run = True

        if command_can_be_run:
            if msg.content.startswith(self.command_prefix):
                command = msg.content.replace(self.command_prefix, "")
                args = shlex.split(command)
                command = args[0]
                args.pop(0)

                for cmd in self.commands:
                    if cmd.name == command or command in cmd.aliases:
                        callback = cmd.get_callback()

                        try: callback(msg, args)
                        except TypeError: callback(msg)
                        except Exception as e: raise exceptions.CommandError(e)

    def register_command(self, **kwargs) -> None:
        """
        Register a command.  

        Args:
            name (str): The name of the command.
            description (str): The description of the command.
            usage (str): The usage of the command.
            aliases (list): A list of aliases for the command.
            callback (func): The callback function for the command. / What the command does.

        Aliases:
            add_command(**kwargs)

        Raises:
            CommandAlreadyExists: If the command already exists.
        """

        name = kwargs["name"]
        description = kwargs["description"] if "description" in kwargs else ""
        usage = kwargs["usage"] if "usage" in kwargs else ""
        aliases = kwargs["aliases"] if "aliases" in kwargs else []
        callback = kwargs["callback"] or kwargs["func"] or kwargs["function"]

        for cmd in self.commands:
            if name in aliases:
                raise ValueError("Command name and aliases cannot be the same.")

            if cmd.name == name:
                raise exceptions.CommandAlreadyExists("Command name already exists.")

        self.commands.append(command.Command(name, description, usage, aliases, callback))
        self.socket.on(events.Events().get_event("on_message"), self._command_event_handler)

    def register_cog(self, cog):
        """
        Register a cog.  
        The class in the cog must be called Commands.  

        Args:
            cog (str): The name of the cog file.

        Aliases:
            add_cog(cog)
        """

        lib = importlib.import_module(cog)
        commands_class = getattr(lib, "Commands")

        commands = commands_class(self)
        commands.register()

    def event(self, *args):
        eventname = args[0].__name__

        if not events.Events().is_valid_event(eventname):
            raise exceptions.InvalidEvent("Event name is invalid.")

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

            self.register_command(command_name, command_description, command_usage, command_aliases, func)

            return func
        return decorator

    add_command = register_command
    add_cog = register_cog