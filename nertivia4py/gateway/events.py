class Events:
    def __init__(self):
        self.events = []

        self.events.append({"on_connect": "connect"})
        self.events.append({"on_disconnect": "disconnect"})
        self.events.append({"on_reconnect": "reconnecting"})
        self.events.append({"on_success": "success"})
        self.events.append({"on_auth_error": "auth_err"})

        self.events.append({"on_message": "receiveMessage"})
        self.events.append({"on_message_delete": "delete_message"})
        self.events.append({"on_message_edit": "update_message"})

        self.events.append({"on_reaction_add": "message:add_reaction"})
        self.events.append({"on_reaction_update": "message:update_reaction"})

        self.events.append({"on_notification_dismiss": "notification:dismiss"})

        self.events.append({"on_channel_create": "channel:created"})
        self.events.append({"on_channel_remove": "channel:remove"})
        self.events.append({"on_channel_mute": "channel:mute"}) 
        self.events.append({"on_channel_unmute": "channel:unmute"})

        self.events.append({"on_server_channel_create": "server:add_channel"})
        self.events.append({"on_server_channel_remove": "server:remove_channel"})
        self.events.append({"on_server_channel_update": "server:update_channel"})
        self.events.append({"on_server_channel_position_update": "server:channel_position"})
        
        self.events.append({"on_server_position_update": "self:server_position"})
        self.events.append({"on_server_add_role": "serverMember:add_role"})
        self.events.append({"on_server_join": "server:joined"})
        self.events.append({"on_server_leave": "server:leave"})
        self.events.append({"on_server_mute": "server:mute"})

        self.events.append({"on_server_members": "server:members"})
        self.events.append({"on_server_roles": "server:roles"})

        self.events.append({"on_roles_update": "server:update_roles"})
        self.events.append({"on_role_create": "server:create_role"})
        self.events.append({"on_role_delete": "server:delete_role"})
        self.events.append({"on_role_update": "server:update_role"})

        self.events.append({"on_server_member_role_remove": "serverMember:remove_role"})

        self.events.append({"on_member_join": "server:member_add"})
        self.events.append({"on_member_leave": "server:member_remove"})

        self.events.append({"on_self_status_update": "multi_device_status"})
        self.events.append({"on_self_custom_status_update": "multi_device_custom_status"})

        self.events.append({"on_user_blocked": "user:block"})
        self.events.append({"on_user_unblocked": "user:unblock"})

        self.events.append({"on_user_joined_call": "user:joined_call"})
        self.events.append({"on_user_left_call": "user:left_call"})
        self.events.append({"on_voice_receive_signal": "voice:receive_signal"})
        self.events.append({"on_voice_receive_return_signla": "voice:receive_return_signal"})

        self.events.append({"on_google_drive_linked": "googleDrive:linked"})

        self.events.append({"on_user_status_update": "user_status_change"})
        self.events.append({"on_user_custom_status_update": "member:custom_status_change"})

        self.events.append({"on_relationship_add": "relationship_add"})
        self.events.append({"on_relationship_remove": "relationship_remove"})
        self.events.append({'on_relationship_accept': 'relationship_accept'})

        self.events.append({"on_custom_emoji_renamed": "ustomEmoji:rename"})
        self.events.append({"on_custom_emoji_uploaded": "ustomEmoji:upload"})
        self.events.append({"on_custom_emoji_deleted": "ustomEmoji:remove"})

        self.events.append({"on_program_activity_update": "programActivity:changed"})

        self.events.append({"on_button_click": "message_button_clicked"})
        self.events.append({"on_button_click_callback": "message_button_click_callback"})