import GroupMe
import discord
from datetime import datetime
from locals import *


class GroupMeHandler:
    def __init__(self, client, group_list):
        self.client = client
        self.group_list = group_list

        # Implement single group polling per tick to improve latency
        self.poll_index = 0

    async def poll_groups(self):
        for group in self.group_list:
            group_text_channel = self.client.get_channel(group.text_channel_id)
            messages_received = group.poll()['messages']
            # Skip the group if there are no new updates
            if len(messages_received) < 1:
                continue
            # Loop through them backwards to send them in the correct order
            for i in range(-1, -1-len(messages_received), -1):
                await self.post_formatted_message(messages_received[i], group_text_channel)

    async def post_formatted_message(self, message, group_text_channel):
        #if message['sender_id'] == USERID_GROUPME:
        #    return

        content = message['text'] if message['text'] is not None else ""
        fields = []
        image = {}
        for attachment in message['attachments']:
            if attachment['type'] == "image":
                image['url'] = attachment['url']
            else:
                # TODO - Impletement other attachment types in the future
                field = {
                    "name": attachment['type'].upper(),
                    #"value": attachment['']
                }

        timestamp = datetime.fromtimestamp(message['created_at']).strftime("%A, %B %d, %Y %I:%M:%S")
        color = 16777215 if message['sender_id'] != USERID_GROUPME else 777215  # 777215 (pretty other color)
        nonce = message['id']
        embed = {
            "author": {
                "name": message['name'],
                "icon_url": message['avatar_url']
            },
            "footer": {
                "text": timestamp
            },
            "description": content,
            "color": color,
            "fields": fields,
            "image": image
        }
        await group_text_channel.send(embed=discord.Embed.from_dict(embed), nonce=nonce)
