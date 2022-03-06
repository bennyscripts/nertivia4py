from . import server
from . import textchannel
from . import user

class Get:
    
    def get_server(id) -> server.Server:
        """
        Gets a Nertivia server.

        Args:
            id (int): The ID of the server.

        Returns:
            server.Server: The server.
        """

        return server.Server(id)

    def get_text_channel(id) -> textchannel.TextChannel:
        """
        Gets a Nertivia text channel.

        Args:
            id (int): The ID of the text channel.

        Returns:
            textchannel.TextChannel: The text channel.
        """

        return textchannel.TextChannel(id)

    def get_user(id) -> user.User:
        """
        Gets a Nertivia user.

        Args:
            id (int): The ID of the user.
                
        Returns:
            user.User: The user.
        """

        return user.User(id)