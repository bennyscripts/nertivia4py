class Events:
    def __init__(self):
        self.custom_events = ["on_command", "on_command_error"]

        self.events = [{"on_success": "authenticated"}, {"on_ready": "authenticated"}, {"on_auth_error": "authentication_error"}, {"on_message": "message:created"}, {"on_message_delete": "message:deleted"}, {"on_message_bulk_delete": "message:deleted_bulk"}, {"on_message_edit": "message:updated"}, {"on_reaction_update": "message:reaction_updated"}, {"on_notification_dismiss": "notification:dismiss"}, {"on_channel_create": "channel:created"}, {"on_channel_remove": "channel:removed"}, {"on_channel_mute": "channel:muted"}, {"on_channel_unmute": "channel:unmuted"}, {"on_server_channel_create": "server:channel_created"}, {"on_server_channel_remove": "server:channel_deleted"}, {"on_server_channel_update": "server:channel_updated"}, {"on_server_channel_position_update": "server:channel_position_updated"}, {"on_server_position_update": "self:position_updated"}, {"on_server_join": "server:joined"}, {"on_server_leave": "server:left"}, {"on_server_mute": "server:muted"}, {"on_server_members": "server:members"}, {"on_server_roles": "server:roles"}, {"on_roles_update": "server:roles_updated"}, {"on_role_create": "server:role_created"}, {"on_role_delete": "server:role_deleted"}, {"on_role_update": "server:role_updated"}, {"on_server_member_role_remove": "server:role_removed_from_member"}, {"on_server_member_role_add": "server:role_added_to_member"}, {"on_member_join": "server:member_added"}, {"on_member_leave": "server:member_removed"}, {"on_self_status_update": "user:status_changed"}, {"on_self_custom_status_update": "user:custom_status_changed"}, {"on_self_program_activity_update": "user:program_activity_changed"}, {"on_user_blocked": "user:blocked"}, {"on_user_unblocked": "user:unblocked"}, {"on_user_joined_call": "user:call_joined"}, {"on_user_left_call": "user:call_left"}, {"on_voice_receive_signal": "voice:signal_received"}, {"on_voice_receive_return_signla": "voice:return_signal_received"}, {"on_google_drive_linked": "google_drive:linked"}, {"on_user_status_update": "user_status_change"}, {"on_user_custom_status_update": "member:custom_status_change"}, {"on_relationship_add": "relationship:added"}, {"on_relationship_remove": "relationship:removed"}, {'on_relationship_accept': 'relationship:accepted'}, {"on_custom_emoji_renamed": "custom_emoji:renamed"}, {"on_custom_emoji_uploaded": "custom_emoji:uploaded"}, {"on_custom_emoji_deleted": "custom_emoji:removed"}, {"on_button_click": "message_button_clicked"}, {"on_button_click_callback": "message_button_click_callback"}]

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