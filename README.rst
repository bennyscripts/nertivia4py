Nertivia4PY
===========

| A Python wrapper for the Nertivia API.
| Support Nertivia server : https://nertivia.net/i/nertivia4py

   .. rubric:: Install
      :name: install

   ::

      pip install nertivia4py

..

   .. rubric:: Example
      :name: example

   .. code:: python

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

   For more examples, take a look at the examples folder in the github
   repo.
