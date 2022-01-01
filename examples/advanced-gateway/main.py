import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.gateway.Client(prefix, commands_path="commands")

@bot.event
def on_success(event):
    print("Connected!")

@bot.event
def on_message(event):
    message = nertivia4py.Message(event["message"]["messageID"], event["message"]["channelID"])

    if message.content.startswith(prefix):
        command, args = bot.parseMessage(message)
        command = bot.getCommand(command)

        if bot.checkIfCommand(command):
            command.command(message, args)
        else:
            message.reply("Command not found.")

bot.run(token)