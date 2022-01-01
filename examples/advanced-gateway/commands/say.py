import nertivia4py

class Say:
    def __init__(self, bot: nertivia4py.gateway.Client):
        self.bot = bot
        self.name = "say"
        self.description = "Make me say something!"
        self.usage = "[your text]"

    def command(self, message: nertivia4py.Message, args: list):
        message.channel.send(" ".join(args))