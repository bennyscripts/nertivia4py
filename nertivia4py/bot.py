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

        self.other_settings = {
            "on_command_callback": None,
            "on_command_error_callback": None,
            "on_message_callback": None
        }

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

    def _on_message_event_handler(self, event):
        msg = message.Message(event["message"]["messageID"], event["message"]["channelId"])
        command_can_be_run = False
        is_a_command = False
        
        if self.other_settings["on_message_callback"] is not None:
            self.other_settings["on_message_callback"](msg)

        if self.self_bot:
            if msg.creator.id == self.user.id:
                command_can_be_run = True
        else:
            if msg.creator.id != self.user.id:
                command_can_be_run = True

        if msg.content.startswith(self.command_prefix):
            is_a_command = True

        if command_can_be_run:
            if is_a_command:
                command = msg.content.replace(self.command_prefix, "")
                args = shlex.split(command)
                command = args[0]
                args.pop(0)

                for cmd in self.commands:
                    if cmd.name == command or command in cmd.aliases:
                        callback = cmd.get_callback()

                        try: 
                            callback(msg, args)

                        except TypeError: 
                            callback(msg)

                        except Exception as e: 
                            if self.other_settings["on_command_error_callback"] is not None:
                                self.other_settings["on_command_error_callback"](msg, str(e))

                            else:
                                raise exceptions.CommandError(str(e))

                        try:
                            if self.other_settings["on_command_callback"] is not None:
                                self.other_settings["on_command_callback"](msg, cmd)

                        except Exception as e:
                            print(e)

                    else:
                        if self.other_settings["on_command_error_callback"] is not None:

                            command_tried = msg.content.replace(self.command_prefix, "")
                            command_tried = shlex.split(command_tried)[0]

                            self.other_settings["on_command_error_callback"](msg, exceptions.CommandNotFound(f"Command {command_tried} not found."))

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

        description = kwargs["description"] if "description" in kwargs else ""
        usage = kwargs["usage"] if "usage" in kwargs else ""
        aliases = kwargs["aliases"] if "aliases" in kwargs else []
        callback = kwargs["callback"] or kwargs["func"] or kwargs["function"]
        name = kwargs["name"] if "name" in kwargs else callback.__name__

        for cmd in self.commands:
            if name in aliases:
                raise ValueError("Command name and aliases cannot be the same.")

            if cmd.name == name:
                raise exceptions.CommandAlreadyExists("Command name already exists.")

        self.commands.append(command.Command(name, description, usage, aliases, callback))
        self.socket.on(events.Events().get_event("on_message"), self._on_message_event_handler)

    def load_commands(self, **kwargs):
        """
        Load commands from a separate file.

        Args:
            lib_path (str): The path to the file. (example: commands.general)
            commands_class (str): The name of the class in the file. (example: Commands)

        Aliases:
            add_commands(lib_path, commands_class)

        Raises:
            AttributeError: If the class is not found.
        """
    
        if "lib_path" in kwargs:  lib_path = kwargs["lib_path"]
        else: raise AttributeError("lib_path is required.")

        if "commands_class" in kwargs: commands_class = kwargs["commands_class"]
        else: raise AttributeError("commands_class is required.")

        lib = importlib.import_module(lib_path)
        commands_class = getattr(lib, commands_class)
        class_instance = commands_class(self)
        class_instance.register()

    def event(self, *args):
        event_name = args[0].__name__
        event_callback = args[0]
        custom_events = events.Events().custom_events

        if events.Events().is_valid_event(event_name) or event_name in custom_events:
            if event_name == "on_message":
                self.other_settings["on_message_callback"] = event_callback
                self.socket.on(events.Events().get_event(event_name), self._on_message_event_handler)

            elif event_name == "on_command":
                self.other_settings["on_command_callback"] = event_callback
                self.socket.on(events.Events().get_event("on_message"), self._on_message_event_handler)

            elif event_name == "on_command_error":
                self.other_settings["on_command_error_callback"] = event_callback
                self.socket.on(events.Events().get_event("on_message"), self._on_message_event_handler)

            else:
                event = events.Events().get_event(event_name)
                self.socket.on(event, event_callback)

        else:
            raise exceptions.InvalidEvent("Event name is invalid.")

    def command(self, **kwargs):
        def decorator(func):
            command_name = kwargs["name"] if "name" in kwargs else func.__name__
            command_description = kwargs["description"] if "description" in kwargs else ""
            command_usage = kwargs["usage"] if "usage" in kwargs else ""
            command_aliases = kwargs["aliases"] if "aliases" in kwargs else []

            self.register_command(name=command_name, description=command_description, usage=command_usage, aliases=command_aliases, callback=func)

            return func
        return decorator

    add_command = register_command
    add_commands = load_commands
    register_commands = load_commands