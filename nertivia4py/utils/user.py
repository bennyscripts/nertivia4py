import requests

from . import embed
from . import extra
from . import dmchannel

class User:
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
    
    def send_friend_request(self):
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

    def accept_friend_request(self):
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

    def decline_friend_request(self):
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

    def block(self):
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

    def unblock(self):
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

    def dm(self, message, embed: embed.Embed = None):
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