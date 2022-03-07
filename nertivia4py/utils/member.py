from . import server
from . import user

class Member:
    """
Nertivia Member
The same as user.User but has ban and kick functions.

Attributes:
- id (int): The ID of the member.
- username (str): The username of the member.
- tag (str): The tag of the member.
- avatar (str): The avatar of the member.
- type (str): The type of the member.
- server_id (int): The ID of the server the member is in.
    """

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
        """
Bans the member.

Returns:
- bool: Whether the member was banned or not.
        """

        server2 = server.Server(self.server_id)
        return server2.ban_member(user.User(self.id, self.username, self.tag, self.avatar))
    
    def kick(self):
        """
Kicks the member.

Returns:
- bool: Whether the member was kicked or not.
        """

        server2 = server.Server(self.server_id)
        return server2.ban_member(user.User(self.id, self.username, self.tag, self.avatar))