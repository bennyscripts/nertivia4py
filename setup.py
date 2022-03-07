from distutils.core import setup

readme = """
# Nertivia4PY
A Python wrapper for the Nertivia API.  
Support Nertivia server : https://nertivia.net/i/nertivia4py

> ### Install
> ```
> pip install nertivia4py
> ```

> ### Example 
> ```python
> import nertivia4py
> 
> token = "TOKEN_HERE"
> prefix = "!"
> 
> bot = nertivia4py.Bot(prefix)
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
"""

setup(
    name='nertivia4py',
    packages=['nertivia4py', 'nertivia4py.gateway', 'nertivia4py.utils', 'nertivia4py.commands'],
    version='1.0.6',
    license='MIT',
    description='A Python wrapper for the Nertivia API',
    long_description_content_type="text/markdown",
    long_description=readme,
    author='Ben Tettmar',
    author_email='hello@benny.fun',
    url='https://github.com/bentettmar/nertivia4py',
    keywords=["nertivia", "api", "wrapper", "python",
              "bot", "nertivia.py", "nertivia4py"],
    install_requires=["requests", 'python-socketio[client]'],
)
