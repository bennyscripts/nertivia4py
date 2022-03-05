import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.gateway.Client(prefix)

@bot.event
def on_success(event):
    print("Connected!")

@bot.command(name="ping", description="Ping command.")
def ping_command(message, args):
    message.reply("Pong!")

@bot.command(name="echo", description="Make the user say something.", usage="<text>")
def echo_command(message, args):
    message.channel.send(args[0])

bot.run(token)
