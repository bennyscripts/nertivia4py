nertivia4py.utils.TextChannel
=============================
Attributes:
    id (int): The ID of the channel.
    name (str): The name of the channel.
    server_id (int): The ID of the server.


send(content, embed, buttons)
-----------------------------
Sends a message to the channel.

Args:
    content (str): The content of the message.
    embed (embed.Embed): The embed of the message.
    buttons (list): A list of buttons to add to the message.

Aliases:
    send_message(content, embed, buttons)

Returns:
    message.Message: The message that was sent.


edit(name)
----------
Edits the channel

Args:
    name (str): The new name of the channel.

Returns:
    dict: The response of the request.


delete()
--------
Deletes the channel.

Returns:
    dict: The response of the request.


typing()
--------
Tells the channel that the user is typing.

Returns:
    requests response: The response of the request.


get_messages(amount)
--------------------
Gets the messages from the channel.

Args:
    amount (int): The amount of messages to get.

Returns:
    list: The messages.


get_message(id)
---------------
Gets a message from the channel.

Args:
    id (int): The ID of the message.
        
Returns:
    message.Message: The message.
    None: If the message doesn't exist.