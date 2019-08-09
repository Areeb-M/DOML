from locals import *
import discord
import GroupMe


class DiscordClient(discord.Client):
    async def on_ready(self):
        await self.update_channels()

    async def on_message(self, message):
        print(message.content)

    async def update_channels(self):
        # Get all the server channels by category
        channel_categories = self.guilds[0].by_category()

        # Get list of top 10 GroupMe chats
        top_groupme_chats = GroupMe.retrieve_groups()

        # Check whether a channel exists for each of them
        for server in top_groupme_chats["response"]:
            print(server)
        for category, channels in channel_categories:
            print(category.name)

    async def create_group_channel(self, name, group_id):
        pass