import requests

from . import embed
from . import extra
from . import dmchannel

class User:
    """
Nertivia User

Attributes:
- id (int): The ID of the user.
- username (str): The username of the user.
- tag (str): The tag of the user.
- avatar (str): The avatar of the user.
- banner (str): The banner of the user.
- created (str): The date the user was created.
- blocked (bool): Whether the user is blocked or not.
    """

    def __init__(self, id, username="", tag="", avatar="", banner="", created="", blocked="") -> None:
        if username == "" or tag == "" or avatar == "":
            response = requests.get(f"https://nertivia.net/api/user/{id}", headers={"Authorization": extra.Extra.getauthtoken()})
            self.id = response.json()["user"]["id"]
            self.avatar = response.json()["user"]["avatar"]
            try:
                self.banner = response.json()["user"]["banner"]
            except:
                pass
            self.username = response.json()["user"]["username"]
            self.tag = response.json()["user"]["tag"]
            try:
                self.created = response.json()["user"]["created"]
            except:
                pass
            try:
                self.blocked = response.json()["isBlocked"]
            except:
                pass
        else:
            self.id = id
            self.avatar = avatar
            self.banner = banner
            self.username = username
            self.tag = tag
            self.created = created
            self.blocked = blocked
        self.avatar_url = f"https://media.nertivia.net/{self.avatar}"
        self.mention = f"[@:{self.id}]"

    def __str__(self) -> str:
        return f"{self.username}:{self.tag}"
    
    def __repr__(self) -> str:
        return f"{self.username}:{self.tag}"
    
    def send_friend_request(self) -> dict:
        """
        Send a friend request to the user.

        Returns:
        - dict: The response of the request.
        """

        response = requests.post(
            "https://nertivia.net/api/user/relationship",
            headers={
                "Authorization": extra.Extra.getauthtoken(),
                "Content-Type": "application/json"
            },
            json={
                "username": self.username,
                "tag": self.tag
            }
        )

        return response.json()

    def accept_friend_request(self) -> dict:
        """
Accept a friend request from the user.

Returns:
- dict: The response of the request.
        """

        response = requests.put(
            "https://nertivia.net/api/user/relationship",
            headers={
                "Authorization": extra.Extra.getauthtoken(),
                "Content-Type": "application/json"
            },
            json={
                "id": self.id
            }
        )
        
        return response.json()

    def decline_friend_request(self) -> dict:
        """
Decline a friend request from the user.

Returns:
- dict: The response of the request.
        """

        response = requests.delete(
            "https://nertivia.net/api/user/relationship",
            headers={
                "Authorization": extra.Extra.getauthtoken(),
                "Content-Type": "application/json"
            },
            json={
                "id": self.id
            }
        )

        return response.json()

    def block(self) -> dict:
        """
        Block the user.

        Returns:
        - dict: The response of the request.
        """

        response = requests.post(
            "https://nertivia.net/api/user/block",
            headers={
                "Authorization": extra.Extra.getauthtoken(),
                "Content-Type": "application/json"
            },
            json={
                "id": self.id
            }
        )

        return response.json()

    def unblock(self) -> dict:
        """
Unblock the user.

Returns:
- dict: The response of the request.
        """

        response = requests.delete(
            "https://nertivia.net/api/user/block",
            headers={
                "Authorization": extra.Extra.getauthtoken(),
                "Content-Type": "application/json"
            },
            json={
                "id": self.id
            }
        )

        return response.json()

    def dm(self, message, embed: embed.Embed = None) -> dict:
        """
Send a direct message to the user.

Args:
- message (str): The message to send.
- embed (embed.Embed): The embed to send.

Aliases:
- send_message(message, embed)
- send_dm(message, embed)
- send(message, embed)

Returns:
- dict: The response of the request.
        """

        response = requests.post(
            f"https://nertivia.net/api/channels/{self.id}",
            headers={
                "Authorization": extra.Extra.getauthtoken(),
                "Content-Type": "application/json"
            }
        )

        channel = dmchannel.DMChannel(response.json()["channel"]["channelId"])
        
        return channel.send(message, embed=embed)
    
    send_message = dm
    send_dm = dm
    send = dm