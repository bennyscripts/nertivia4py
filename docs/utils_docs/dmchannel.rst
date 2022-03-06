nertivia4py.utils.DMChannel
===========================
Same as Text Channel but is used to send messages to a user.

Attributes:
    id (int): The ID of the channel.


send(content, embed, buttons)
-----------------------------
Sends a message to the channel.

Args:
    content (str): The content of the message.
    embed (embed.Embed): The embed of the message.
    buttons (list): The buttons of the message.

Aliases:
    send_message(content, embed, buttons)
    
Returns:
    dict: The response of the request.