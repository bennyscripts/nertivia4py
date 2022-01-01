Nertivia4PY
===========

A Python wrapper for the Nertivia API

Install
~~~~~~~

::

   pip install nertivia4py

Examples
~~~~~~~~

Basic example for just controlling the API step by step.

.. code:: python

   import nertivia4py

   channel_id = 123
   token = "TOKEN_HERE"

   bot = nertivia4py.Nertivia(token)
   channel = bot.getChannel(channel_id)

   channel.send("Hello World!")

Basic example for connecting to the gateway.

.. code:: python

   import nertivia4py

   token = "TOKEN_HERE"
   prefix = "."

   bot = nertivia4py.gateway.Client(prefix)

   @bot.event
   def on_connect(event):
       print("Connected!")

   @bot.event
   def on_message(event):
       message = nertivia4py.Message(event["message"]["messageID"], event["message"]["channelID"])
       print(message.content)

       if message.content.startswith(prefix):
           command = message.content.split(" ")[0][1:]

           if command == "ping":
               message.reply("pong!")

   bot.run(token)

For more examples, take a look at the examples folder in the github
repo.
