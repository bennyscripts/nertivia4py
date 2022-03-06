nertivia4py.utils.Server
========================
Attributes:
    id (str): The server's ID.
    name (str): The server's name.
    avatar (str): The server's avatar.
    default_channel_id (str): The server's default channel ID.
    created (str): The server's creation date.
    banner (str): The server's banner.


edit(name)
----------
Edits the server

Args:
    name (str): The new name of the server.

Returns:
    dict: The response of the request.


delete()
--------
Deletes the server

Returns:
    dict: The response of the request.


get_bans()
----------
Gets a list of banned users from the server

Returns:
    list: A list of banned users.
    None: If the request failed.


ban_member(user)
----------------
Bans a member from the server

Args:
    user (user.User): The user to ban.

Returns:
    bool: Whether the request was successful.


kick_member(user)
-----------------
Kicks a member from the server

Args:
    user (user.User): The user to Kick.

Returns:
    bool: Whether the request was successful.


unban_member(user)
------------------
Unbans a member from the server

Args:
    user (user.User): The user to unban.

Returns:
    bool: Whether the request was successful.


get_members()
-------------
Gets a list of members from the server

Aliases:
    get_all_members()

Returns:
    list: A list of members.


get_channels()
--------------
Gets a list of channels from the server

Aliases:
    get_all_channels()

Returns:
    list: A list of channels.


create_text_channel(name)
-------------------------
Creates a text channel in the server.

Args:
    name (str): The name of the channel.
        
Returns:
    textchannel.TextChannel: The channel that was created.