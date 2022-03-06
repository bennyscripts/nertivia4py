An example of `load_commands()`.  
`load_commands()` is used to load a commands class from a separate file.  

View how its used in `bot.py` and `commands/general.py`.  

```
load_commands()
Load commands from a separate file.

Args:
    lib_path (str): The path to the file. (example: commands.general)
    commands_class (str): The name of the class in the file. (example: Commands)

Aliases:
    add_commands(lib_path, commands_class)

Raises:
    AttributeError: If the class is not found.
```