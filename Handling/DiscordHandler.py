import discord
from GroupMe import construct_message
from locals import *


class DiscordHandler(object):
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        print(message.content, message.author)
        if message.channel.category == self.client.group_category and str(message.author) == NAME_DISCORD:
            group = self.client.group_cache[message.channel]
            for attachment in message.attachments:
                group_message = construct_message(attachment.url)
                group.send(group_message)

            if message.content != "":
                group_message = construct_message(message.content)
                group.send(group_message)

            # Remove the message after processing
            await message.delete()
