from . import server
from . import user

class Member:
    def __init__(self, id, username="", tag="", avatar="", type="", server_id="") -> None:
        self.id = id
        self.username = username
        self.tag = tag
        self.avatar = avatar
        self.type = type
        self.server_id = server_id

    def __str__(self) -> str:
        return f"{self.username}:{self.tag}"

    def ban(self):
        server2 = server.Server(self.server_id)
        return server2.ban_member(user.User(self.id, self.username, self.tag, self.avatar))
    
    def kick(self):
        server2 = server.Server(self.server_id)
        return server2.ban_member(user.User(self.id, self.username, self.tag, self.avatar))