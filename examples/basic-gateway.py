import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.gateway.Client(prefix)

@bot.event
def on_success(event):
    print("Connected!")

def ping_command(message, args):
    message.reply("Pong!")

def echo_command(message, args):
    message.reply(args[0])

bot.register_command("ping", ping_command)
bot.register_command("echo", echo_command)

bot.run(token)
