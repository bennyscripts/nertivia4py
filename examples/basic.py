import nertivia4py

channel_id = 123
token = "TOKEN_HERE"

bot = nertivia4py.Nertivia(token)
channel = bot.getChannel(channel_id)

channel.send("Hello World!")