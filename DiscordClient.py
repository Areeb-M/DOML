from locals import *
import GroupMe
from time import time
from Handling import DiscordHandler, GroupMeHandler
from asyncio import sleep


class DiscordClient(discord.Client):
    def __init__(self, time_between_refresh=60):
        self.group_list = GroupMe.Group.generate_group_list(retrieve_group_data())
        self.group_cache = {}
        self.guild = None
        self.group_category = None

        self.discord_handler = DiscordHandler.DiscordHandler(self)
        self.groupme_handler = GroupMeHandler.GroupMeHandler(self, self.group_list)

        self.time_between_refresh = time_between_refresh
        self.time_last_refresh = 0  # Have a refresh happen immediately

        super().__init__()

    async def on_ready(self):
        self.guild = self.guilds[0]
        self.group_category = await self.find_category_channel("GroupMe Servers")
        await self.update_channels()
        self.generate_group_cache()

        # Make sure this function is started on the first pass of the event loop
        self.loop.create_task(self.tick())

    async def on_message(self, message):
        # Pass through to DiscordHandler
        await self.discord_handler.on_message(message)

    async def update_channels(self):
        # Get all the server channels by category
        #channel_categories = self.guilds[0].by_category()

        # Get list of top 10 GroupMe chats
        top_groupme_chats = GroupMe.retrieve_groups()

        # Check whether a channel exists for each of them
        for server_data in top_groupme_chats:
            if server_data["group_id"] not in self.group_list:
                await self.create_group_channel(server_data)

        store_group_data(self.group_list)
        #for category, channels in channel_categories:
        #    print(category.name)

    async def create_group_channel(self, server_data):
        # Scrape important information
        group_id = server_data["group_id"]
        name = server_data["name"]
        description = server_data["description"]

        # Create a Discord Text Channel for it
        channel = await self.group_category.create_text_channel(name, topic=description)

        # Create Group Object
        group = GroupMe.Group(group_id, channel.id)

        # Add Group Object to group list and save file
        self.group_list.append(group)
        append_group_data(group)

    async def find_category_channel(self, name):
        result = None
        for category in self.guild.categories:
            if category.name == name:
                result = category
                return result

        if result is None:
            print("Category Channel {} not found, generating...".format(name))
            result = await self.guild.create_category_channel(name)
            return result

    def generate_group_cache(self):
        for group in self.group_list:
            channel = self.guild.get_channel(group.text_channel_id)
            self.group_cache[channel] = group

    async def tick(self):
        tick_count = 0
        while True:
            # Refresh Group List every <self.time_between_refresh> seconds
            if time() - self.time_last_refresh > self.time_between_refresh:
                await self.update_channels()
                self.generate_group_cache()
                self.time_last_refresh = time()

            tick_count += 1
            print("tick {}".format(tick_count))

            # Check groups for new messages and post them
            await self.groupme_handler.poll_groups()

            # Hand off to the main loop
            await sleep(0.1)
