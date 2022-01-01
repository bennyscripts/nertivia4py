import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.gateway.Client(prefix)

@bot.event
def on_success(event):
    print("Connected!")

@bot.event
def on_message(event):
    message = nertivia4py.Message(event["message"]["messageID"], event["message"]["channelID"])

    if message.content.startswith(prefix):
        command = message.content.split(" ")[0][1:]

        if command == "ping":
            message.reply("pong!")

bot.run(token)
