# Nertivia4PY
A Python wrapper for the Nertivia API.  
Support Nertivia server : https://nertivia.net/i/nertivia4py

> ### Install
> ```
> pip install nertivia4py
> ```

> ### Examples
> Basic example for just controlling the API step by step.  
> ```python
> import nertivia4py
> 
> channel_id = 123
> token = "TOKEN_HERE"
> 
> bot = nertivia4py.Nertivia(token)
> channel = bot.get_channel(channel_id)
> 
> channel.send("Hello World!")
> ``` 
> 
> Basic example for connecting to the gateway.  
> ```python
> import nertivia4py
> 
> token = "TOKEN_HERE"
> prefix = "!"
> 
> bot = nertivia4py.gateway.Client(prefix)
> 
> @bot.event
> def on_success(event):
>     print("Connected!")
> 
> @bot.command(name="ping", description="Ping command.")
> def ping_command(message, args):
>     message.reply("Pong!")
> 
> bot.run(token)
> ```  
> 
> For more examples, take a look at the examples folder in the github repo.
