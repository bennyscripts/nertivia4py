import nertivia4py

token = "TOKEN_HERE"
prefix = "!"

bot = nertivia4py.Bot(prefix)

@bot.event
def on_success(event):
    print("Connected!")

bot.load_commands("commands.general", "GeneralCommands") # If the commands class was called Commands you would not need to specify the class name.
bot.run(token)
