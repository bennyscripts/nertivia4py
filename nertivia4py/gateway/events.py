class Events:
    def __init__(self):
        self.events = []
        self.custom_events = []

        self.custom_events.append("on_command")
        self.custom_events.append("on_command_error")

        self.events.append({"on_success": "authenticated"})
        self.events.append({"on_ready": "authenticated"})
        self.events.append({"on_auth_error": "authentication_error"})

        self.events.append({"on_message": "message:created"})
        self.events.append({"on_message_delete": "message:deleted"})
        self.events.append({"on_message_bulk_delete": "message:deleted_bulk"})
        self.events.append({"on_message_edit": "message:updated"})

        # self.events.append({"on_reaction_add": "message:add_reaction"})
        self.events.append({"on_reaction_update": "message:reaction_updated"})

        self.events.append({"on_notification_dismiss": "notification:dismiss"})

        self.events.append({"on_channel_create": "channel:created"})
        self.events.append({"on_channel_remove": "channel:removed"})
        self.events.append({"on_channel_mute": "channel:muted"}) 
        self.events.append({"on_channel_unmute": "channel:unmuted"})

        self.events.append({"on_server_channel_create": "server:channel_created"})
        self.events.append({"on_server_channel_remove": "server:channel_deleted"})
        self.events.append({"on_server_channel_update": "server:channel_updated"})
        self.events.append({"on_server_channel_position_update": "server:channel_position_updated"})
        
        self.events.append({"on_server_position_update": "self:position_updated"})
        self.events.append({"on_server_join": "server:joined"})
        self.events.append({"on_server_leave": "server:left"})
        self.events.append({"on_server_mute": "server:muted"})

        self.events.append({"on_server_members": "server:members"})
        self.events.append({"on_server_roles": "server:roles"})

        self.events.append({"on_roles_update": "server:roles_updated"})
        self.events.append({"on_role_create": "server:role_created"})
        self.events.append({"on_role_delete": "server:role_deleted"})
        self.events.append({"on_role_update": "server:role_updated"})

        self.events.append({"on_server_member_role_remove": "server:role_removed_from_member"})
        self.events.append({"on_server_member_role_add": "server:role_added_to_member"})

        self.events.append({"on_member_join": "server:member_added"})
        self.events.append({"on_member_leave": "server:member_removed"})

        self.events.append({"on_self_status_update": "user:status_changed"})
        self.events.append({"on_self_custom_status_update": "user:custom_status_changed"})
        self.events.append({"on_self_program_activity_update": "user:program_activity_changed"})

        self.events.append({"on_user_blocked": "user:blocked"})
        self.events.append({"on_user_unblocked": "user:unblocked"})

        self.events.append({"on_user_joined_call": "user:call_joined"})
        self.events.append({"on_user_left_call": "user:call_left"})
        self.events.append({"on_voice_receive_signal": "voice:signal_received"})
        self.events.append({"on_voice_receive_return_signla": "voice:return_signal_received"})

        self.events.append({"on_google_drive_linked": "google_drive:linked"})

        self.events.append({"on_user_status_update": "user_status_change"})
        self.events.append({"on_user_custom_status_update": "member:custom_status_change"})

        self.events.append({"on_relationship_add": "relationship:added"})
        self.events.append({"on_relationship_remove": "relationship:removed"})
        self.events.append({'on_relationship_accept': 'relationship:accepted'})

        self.events.append({"on_custom_emoji_renamed": "custom_emoji:renamed"})
        self.events.append({"on_custom_emoji_uploaded": "custom_emoji:uploaded"})
        self.events.append({"on_custom_emoji_deleted": "custom_emoji:removed"})

        self.events.append({"on_button_click": "message_button_clicked"})
        self.events.append({"on_button_click_callback": "message_button_click_callback"})

    def get_event(self, event_name):
        for event in self.events:
            for key, value in event.items():
                if key == event_name:
                    return value

    def get_event_name(self, event_value):
        for event in self.events:
            for key, value in event.items():
                if value == event_value:
                    return key

    def is_valid_event(self, event_name):
        for event in self.events:
            for key, value in event.items():
                if key == event_name:
                    return True
        return False