from . import server
from . import channel
from . import user

def get_server(id) -> server.Server:
    return server.Server(id)

def get_channel(id) -> channel.Channel:
    return channel.Channel(id)

def get_user(id) -> user.User:
    return user.User(id)