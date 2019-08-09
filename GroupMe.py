from random import randint
from locals import *
from json import loads


class Group(object):
    pass


class Chat(object):
    pass


def retrieve_groups(number=10, page=1):
    data = {"per_page": str(number), "page": str(page)}
    post = requests.get('https://api.groupme.com/v3/groups?token=' + TOKEN_GROUPME, json=data)
    return loads(post.content)


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
    post = requests.post('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + TOKEN_GROUPME,
                         json=message)
    return post


def post_message_to_chat(user_id, direct_message):
    direct_message["direct_message"]["recipient_id"] = user_id
    post = requests.post('https://api.groupme.com/v3/direct_messages?token=' + TOKEN_GROUPME,
                         json=direct_message)
    return post
