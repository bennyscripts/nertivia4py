from distutils.core import setup

readme = """
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
"""

setup(
    name='nertivia4py',
    packages=['nertivia4py'],
    version='0.1',
    license='MIT',
    description='A Python wrapper for the Nertivia API',
    long_description_content_type="text/markdown",
    long_description=readme,
    author='Ben Tettmar',
    author_email='hello@benny.fun',
    url='https://github.com/bentettmar/nertivia4py',
    keywords=["nertivia", "api", "wrapper", "python",
              "bot", "nertivia.py", "nertivia4py"],
    install_requires=["requests", '"python-socketio[client]"'],
    classifiers=[
        'Development Status :: 3 - Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
