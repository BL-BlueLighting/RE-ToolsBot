from nonebot import *
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.permission import SUPERUSER
import nonebot,random,json,requests
from time import sleep as wait
from random import uniform as wrd
import os
from nonebot.typing import *
import dauCtl as dc

config = json.load(open("./data/configuration.json", "r", encoding="utf-8"))
"""
welcom=on_notice()
 
@welcom.handle()
async def welcome(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = "欢迎！：[CQ:at,qq={}]".format(user)
    msg = at_ + '大佬加入'
    msg = Message(msg)
    if event.group_id == 1014764229:#在这里写上你的群号
        await welcom.finish(message=Message(f'{msg}'))
"""

def replacing(string: str, qqNumber: str) -> str:
    # replacing string using qqNumber and CQ:at
    res = string
    res.replace("[QQ]", qqNumber)
    res.replace("[@]", f"[CQ:at,qq={qqNumber}]")
    return res

welcomejoin_event = on_notice()

@welcomejoin_event.handle()
async def welcome(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    # if new user join, auto make a new archive.
    dc.User(user, score=50) # present 50 scores.
    
    await welcomejoin_event.finish(replacing(config ["WelcomeMessage"], user))

goodbye_event = on_notice()

@goodbye_event.handle()
async def goodbye(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    await goodbye_event.finish(replacing(config ["GoodbyeMessage"], user))

# auto agree friend adding

friend_add = on_metaevent()

@friend_add.handle()
async def addfriend(bot: Bot, event: FriendRequestEvent, state: T_State):
    await event.approve(bot) # auto approve, f**king nonebot type comments #type: ignore

async def mute_sb(bot: Bot, gid: int, lst: list, time: int = None, scope: list = None): #type: ignore
    """
    构造禁言
    :param gid: 群号
    :param time: 时间（s)
    :param lst: at列表
    :param scope: 用于被动检测禁言的时间范围
    :return:禁言操作
    """
    # 感谢 https://github.com/yzyyz1387/nonebot_plugin_admin/ 该项目
    su = SUPERUSER
    if 'all' in lst:
        yield bot.set_group_whole_ban(group_id=gid, enable=True)
    else:
        if time is None:
            if scope is None:
                time = random.randint(plugin_config.ban_rand_time_min, plugin_config.ban_rand_time_max)
            else:
                time = random.randint(scope[0], scope[1])
        for qq in lst:
            if qq in su:
                logger.info(f"SUPERUSER无法被禁言, {qq}")
            else:
                yield bot.set_group_ban(group_id=gid, user_id=qq, duration=time)
                
                
async def getReply(content: Message):
    # extract plaintext
    pt = content.extract_plain_text()
    # search
    if not "[reply:id" in pt:
        return "not found"
    
    # split
    reply_c = pt [pt.index("[reply:id"):pt.index("]")]
    
    # remove [reply:id]
    reply_c = reply_c.replace("[reply:id", "")
    reply_c = reply_c.replace("]", "")
    
    # return message id
    return reply_c
    
# undo message

undo_message = on_command("undo", permission=SUPERUSER)
@undo_message.handle()
async def undo_msg(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    # get message
    reply = getReply(args)
    
    if reply == "not found":
        await undo_message.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 请回复一条消息再进行撤回")
    
    try:
        await bot.delete_msg(message_id=reply)
    except ActionFailed:
        await undo_message.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 无法撤回该条消息。请确认 Bot 拥有管理员权限。")
    else:
        await undo_message.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 成功撤回该消息。")
    return

"""
检测at了谁，返回[qq, qq, qq,...]
包含全体成员直接返回['all']
如果没有at任何人，返回[]
:param data: event.json
:return: list

@author: Unk, Not me
"""

def At(data: str):
    try:
        qq_list: list = []
        data_: dict = json.loads(data)
        for msg in data_["message"]:
            if msg["type"] == "at":
                if 'all' not in str(msg):
                    qq_list.append(msg["data"]["qq"])
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []
    
# mutesb

mutesb = on_command("mute", permission=SUPERUSER)

@mutesb.handle()
async def mutesb_command(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    sblist = At(event.json())
    SECOND = 60
    
    arg = args.extract_plain_text()
    minutes = arg [arg.index("minute=") + 7:len(arg)]
    
    mute_sb(bot, event.group_id, lst=sblist, time=int(minutes) * SECOND)
    
    await mutesb.finish(f"RE: ToolsBot GROUP MANAGING MODULE\n    - 已禁言 {arg}。")