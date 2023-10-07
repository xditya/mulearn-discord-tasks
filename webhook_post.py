url = "your_webhook_url_here"

import requests

# channels
create_channel = {"type": "channel", "action": "create", "name": "test-channel"}
edit_channel = {
    "type": "channel",
    "action": "edit",
    "name": "test-channel",
    "new_name": "test-channel-edited",
}
delete_channel = {"type": "channel", "action": "delete", "name": "test-channel-edited"}


# roles
create_role = {"type": "role", "action": "create", "name": "test-role"}
edit_role = {
    "type": "role",
    "action": "edit",
    "name": "test-role",
    "new_name": "test-role-edited",
}
delete_role = {"type": "role", "action": "delete", "name": "test-role-edited"}

# post data to webhook
requests.post(
    url,
    data={"content": str(delete_role)},
)
