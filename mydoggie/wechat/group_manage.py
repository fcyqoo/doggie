# coding:utf-8
import itchat
from itchat.content import *


def getGroup():
    pass

chatroom_ids = []
chatrooms = []
config_group_nickname = ['有逼格的娱乐群', '励志勤奋好学小分队']

# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, NOTE], isGroupChat=True)
def group_reply_text(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['ToUserName']

    chatroom_ids, chatrooms = init_monitor_groups()
    msg_from_group_name = ""
    for node in chatrooms:
        if node["UserName"] == chatroom_id:
            msg_from_group_name = node["NickName"]
    print(">>>>>>msg:", msg)
    print(">>>>chatroom_ids, chatrooms:", chatroom_ids, chatrooms)

    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        print("not the group")
        return

    if msg['Type'] == TEXT:
        content = msg['Content']
        if not content.startswith("%千里传音"):
            print("not the magic")
            return

    elif msg['Type'] == NOTE:
        content = msg['Text']

    # 根据消息类型转发至其他群
    if msg['Type'] == TEXT:
        for item in chatrooms:
            if not item['UserName'] == chatroom_id:
                itchat.send('%s\n%s' % ("[" + msg_from_group_name + "]", msg['Content']), item['UserName'])
    elif msg['Type'] == NOTE:
        for item in chatrooms:
            if not item['UserName'] == chatroom_id:
                itchat.send('%s\n%s\n%s' % ("[" + msg_from_group_name + "]", msg['Text'], msg['Url']), item['UserName'])


def init_monitor_groups():
    chatrooms = itchat.get_chatrooms(update=False, contactOnly=False)
    chatroom_ids = []
    chatrooms_filter = []

    # print("get all>>>", chatrooms)
    for c in chatrooms:
        if c['NickName'] in config_group_nickname:
            chatroom_ids.append(c['UserName'])
            chatrooms_filter.append(c)
    return chatroom_ids, chatrooms_filter


def test():
    itchat.auto_login()
    # 绑定消息响应事件后，让itchat运行起来，监听消息
    itchat.run()


if __name__ == "__main__":
    test()