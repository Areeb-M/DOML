from random import randint
from locals import *
from json import loads, JSONDecodeError
from time import time
from urllib3.exceptions import MaxRetryError


class Group(object):
    # To prevent the bot from spamming the GroupMe servers
    TIME_BETWEEN_POLLS = 0.5

    def __init__(self, group_id, text_channel_id, current_message_id=""):
        self.group_id = group_id
        self.text_channel_id = text_channel_id
        self.current_message_id = current_message_id
        self.time_last_poll = 0  # 0 to force an update next event loop

    def send(self, message):
        # TODO - Implement error handling if message isn't posted successfully
        post_message_to_group(self.group_id, message)

    def poll(self):
        empty = {"messages": []}
        if time() - self.time_last_poll < Group.TIME_BETWEEN_POLLS:
            return empty
        self.time_last_poll = time()
        try:
            messages = retrieve_message_from_group(self.group_id, since_id=self.current_message_id)
        except JSONDecodeError:
            # No new messages to receive
            return empty
        try:
            self.current_message_id = messages['messages'][0]['id']
        except TypeError as t:
            print(t, messages)
            return empty
        return messages

    def get_text_channel(self):
        return self.text_channel_id

    def __eq__(self, other):
        if isinstance(other, str):
            return self.group_id == other
        elif isinstance(other, Group):
            return self.group_id == other.group_id
        elif isinstance(other, discord.TextChannel):
            return self.text_channel_id == other.id
        else:
            return False

    def __str__(self):
        data = str(self.__dict__)
        # Convert single quotes to double quotes to account for JSON library
        data = data.replace("'", '"')
        return data

    @staticmethod
    def generate_group_list(data):
        # Input: List of lines from data/list_groups.txt
        # Output: List of Group Objects
        groups = []
        for group in data:
            keys = loads(group)
            groups.append(Group(keys["group_id"], keys["text_channel_id"], keys["current_message_id"]))

        return groups


class Chat(object):
    pass


def retrieve_groups(number=10, page=1):
    # TODO - Fix the parameters for this function's GET request
    data = {"per_page": number, "page": page}
    try:
        post = requests.get('https://api.groupme.com/v3/groups?token=' + TOKEN_GROUPME, json=data)
        return loads(post.content)["response"]
    except ConnectionError:
        print("Failed to retrieve group list from groupme")
        return []
    except KeyError:
        print("Response formatted incorrectly")
        return []


def construct_message(text=""):
    return {
        "message": {
            "source_guid": str(randint(1, 696968)),  # 696968 is a magic number(Thanks Aaron)
            "text": text,
            # TODO - Implement the advanced attachment features of a GroupMe message
        }
    }


def construct_direct_message(text=""):
    return {
        "direct_message": {
            "source_guid": str(randint(1, 696968)),  # 696968 is a magic number(Thanks Aaron)
            "recipient_id": "",
            "text": text,
            # TODO - Implement the advanced attachment features of a GroupMe direct message
        }
    }


def post_message_to_group(group_id, message):
    try:
        post = requests.post('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + TOKEN_GROUPME,
                             json=message)
        return post
    except ConnectionError:
        print("Failed to post message to group")
        return -1  # return status


def post_message_to_chat(user_id, direct_message):
    direct_message["direct_message"]["recipient_id"] = user_id

    try:
        post = requests.post('https://api.groupme.com/v3/direct_messages?token=' + TOKEN_GROUPME,
                             json=direct_message)
        return post
    except ConnectionError:
        print("Failed to post message to chat")
        return -1  # return status


def retrieve_message_from_group(group_id, before_id="", since_id="", after_id="", limit=20):
    empty = '{"messages": []}'
    data = ""
    if before_id != "":
        data += "&before_id=" + before_id
    if since_id != "":
        data += "&since_id=" + since_id
    if after_id != "":
        data += "&after_id=" + after_id
    if limit != 0:
        data += "&limit=" + str(limit)

    try:
        post = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + TOKEN_GROUPME + data)
    except (ConnectionError, MaxRetryError, Exception):
        print("Error polling groupme for chat messages")
        return empty

    try:
        return loads(post.content)['response']
    except KeyError:
        print("response key not found in post")
        return empty


