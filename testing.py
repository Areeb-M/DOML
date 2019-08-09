from locals import *

post = requests.get('https://api.groupme.com/v3/groups?token='+TOKEN_GROUPME, json={})
print(post.content)

post = requests.get('https://api.groupme.com/v3/chats?token='+TOKEN_GROUPME, json={})
print(post.content)

'''
post = requests.post('https://api.groupme.com/v3/groups/21563868/messages?token='+TOKEN_GROUPME,
                     json={"message":
                               {"text": "https://media.tenor.com/images/bea05df7952264ef711c5a344d516adb/tenor.gif"}
                           })
'''
'''
post = requests.post('https://api.groupme.com/v3/groups/51981768/messages?token='+TOKEN_GROUPME,
                     json={"message":
                               {"text": "https://media.giphy.com/media/mjiDIdmMyDhMQ/giphy.gif"}
                           })
'''