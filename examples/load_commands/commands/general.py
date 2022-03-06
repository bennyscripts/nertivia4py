class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot

    def echo_command(self, message, args):
        text = " ".join(args)

        if text:
            message.channel.send(text)
        else:
            message.reply("You need to specify some text.")

    def ping_command(self, message, args):
        message.reply("Pong!")

    def register(self): # This is important! Its needed to register the commands.
        # Setting command names, descriptions, usages and aliases are done the same way as using @bot.command()
        # but you have to pass in the callback/the function that will be called when the command is called.
        # If a command name is not given the command name will be the function name.

        self.bot.register_command(name="echo", description="Make the bot say something.", usage="<text>", callback=self.echo_command)
        self.bot.register_command(name="ping", description="pong!", callback=self.ping_command)

