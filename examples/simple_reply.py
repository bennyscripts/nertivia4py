import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.Bot(prefix)

@bot.event
def on_success(event):
    print("Connected!")

@bot.command(name="ping", description="Ping command.")
def ping_command(message, args):
    message.reply("Pong!")

bot.run(token)
