import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.Bot(prefix)

@bot.event
def on_success(event):
    print("Connected!")

@bot.command(name="echo", description="Make the bot say something.", usage="<text>")
def echo_command(message, args):
    text = " ".join(args)

    if text:
        message.channel.send(text)
    else:
        message.reply("You need to specify some text.")

bot.run(token)