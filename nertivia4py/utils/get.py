from . import server
from . import textchannel
from . import user

def get_server(id) -> server.Server:
    return server.Server(id)

def get_text_channel(id) -> textchannel.TextChannel:
    return textchannel.TextChannel(id)

def get_user(id) -> user.User:
    return user.User(id)