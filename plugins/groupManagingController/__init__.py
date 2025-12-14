import json
import logging
import re
from typing import Union

import nonebot
import nonebot.adapters.onebot.v11
import toml
from nonebot import on_command, on_notice, on_request
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import (FriendRequestEvent,
                                         GroupDecreaseNoticeEvent,
                                         GroupIncreaseNoticeEvent,
                                         GroupMessageEvent)
from nonebot.adapters.onebot.v11 import Message as OneBotMessage
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

import plugins.userInfoController as dc
from toolsbot.configs import DATA_PATH
from toolsbot.services import _crit, _info, _warn

cfg_path = DATA_PATH / "configuration.toml"

with open(cfg_path, "r", encoding="utf-8") as f:
    config = toml.load(f)

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

async def replacing(bot: nonebot.adapters.onebot.v11.Bot, string: str, qqNumber: str) -> str:
    # replacing string using qqNumber and CQ:at
    res = string

    res = res.replace("[@]", "[CQ:at,qq={}]".format(qqNumber))
    # replacing "Name" using api
    try:
        user_info = await bot.call_api("get_user_info", user_id=int(qqNumber))
        res = res.replace("[Name]", user_info["name"])
    except Exception as e:
        _warn(f"Failed to get user info using qq number {qqNumber}. This is why:\n{e}")
        res = res.replace("[Name]", "未知名称")

    return res

async def msg_reply(event: GroupMessageEvent) -> Union[int, None]:
    return event.reply.message_id if event.reply else None

welcomejoin_event = on_notice()

@welcomejoin_event.handle()
async def welcome(bot: nonebot.adapters.onebot.v11.Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()

    # if new user join, auto make a new archive.
    dc.User(user, score=50) # present 50 scores.

    # check if it in banned, auto ban
    if dc.User(user).banned:
        try:
            await bot.call_api("set_group_ban", group_id=event.group_id, user_id = user, duration=2591940)
        except ActionFailed:
            _crit("Failed to auto ban a sb.")

    await welcomejoin_event.finish(OneBotMessage(await replacing(bot, config["WelcomeMessage"], user)))

goodbye_event = on_notice()

@goodbye_event.handle()
async def goodbye(bot: nonebot.adapters.onebot.v11.Bot, event: GroupDecreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    await goodbye_event.finish(OneBotMessage(await replacing(bot, config["EscapeMessage"], user)))

# auto agree friend adding

friend_add = on_request()

@friend_add.handle()
async def addfriend(bot: nonebot.adapters.onebot.v11.Bot, event: FriendRequestEvent, state: T_State):
    await event.approve(bot) # auto approve, f**king nonebot type comments #type: ignore
    await friend_add.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 已通过您的请求。")

undo_message = on_command("undo", permission=SUPERUSER, priority=5)

@undo_message.handle()
async def undo_msg(bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    # get reply id
    reply_id = await msg_reply(event)

    if reply_id == None:
        await undo_message.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 请回复一条消息再撤回")
    # delete msg
    try:
        await bot.call_api("delete_msg", message_id=reply_id)
    except ActionFailed as afd:
        _crit(f"Failed to undo message using msgid。This is why:\n{afd}")
        await undo_message.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 未能成功撤回消息。请确认消息存在或发送人不是管理\\群主\\bot自己（虽然会撤回但是还是会报错）")
    else:
        await undo_message.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 成功撤回消息 msg_id=" + str(reply_id) + "。") #type: ignore


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

mutesb = on_command("mute", permission=SUPERUSER, aliases={"shutup"})

@mutesb.handle()
async def mutesb_command(bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    sblist = At(event.json())
    SECOND = 60

    arg = args.extract_plain_text()
    minutes = arg [arg.index("minute=") + 7:len(arg)]

    _info(sblist)
    _info(arg)
    _info(minutes)
    for qq in sblist:
        try:
            await bot.call_api("set_group_ban", group_id=event.group_id, user_id = qq, duration=float(minutes) * SECOND)
        except ActionFailed:
            await mutesb.finish(f"RE: ToolsBot GROUP MANAGING MODULE\n    - 无法禁言该用户。该用户已被禁言或是管理员\\群主")

    await mutesb.finish(f"RE: ToolsBot GROUP MANAGING MODULE\n    - 已禁言 {sblist} {arg}。")

# unmutesb

unmute = on_command("unmute", permission=SUPERUSER)

@unmute.handle()
async def unmute_command(bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    sblist = At(event.json())

    arg = args.extract_plain_text()

    for qq in sblist:
        await bot.call_api("set_group_ban", group_id=event.group_id, user_id = qq, duration=0)

    await mutesb.finish(f"RE: ToolsBot GROUP MANAGING MODULE\n    - 已取消禁言 {sblist} {arg}。")

# call_api

call_api_command = on_command("call_api", permission=SUPERUSER)

@call_api_command.handle()
async def _ (bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    # get api name and params
    __argstr = args.extract_plain_text()

    # extract api name and params
    api_name = __argstr.split(" ") [0]
    api_params = __argstr.split(" ") [1:]

    # params text
    params_text = ""

    for param in api_params:
        if params_text == "":
            params_text += param
        else:
            params_text += f",{param}"

    # run
    exec(f"""bot.call_api('{api_name}', {params_text})""")

    # finish
    await call_api_command.finish("RE: ToolsBot GROUP MANAGING MODULE\n    - 已执行该 OneBot V11 api。请检查控制台。")

# test admin permission
test_admin = on_command("testadmin", permission=SUPERUSER)

@test_admin.handle()
async def _ (bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    # direct run onebot api
    admin_list = await bot.call_api("get_group_member_info", group_id=event.group_id, user_id=bot.self_id)
    await test_admin.finish(f"RE: ToolsBot GROUP MANAGING MODULE\n    - 该 Bot 在本群的权限是 {admin_list['role']}。")

"""
棍母检测 函数

Checking for otto mother.

在 configuration.toml 中设置 "openOttoMother": true 来开启
@author: Latingtude
"""

# 棍母拼音对应的汉字集合
GUNMU_CHARS = "棍滚丨木母牧姆慕墓暮募幕目沐穆拇"

def replace_gunmu(text: str) -> str:
    # 匹配所有拼音为 gun 或 mu 的常见汉字
    pattern = f"[{GUNMU_CHARS}]"
    return re.sub(pattern, "█", text)

with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = toml.load(f)
    _info(cfg)
    _info(cfg.get("openOttoMother"))
"""
otto_mother = on_message(priority=1, block=False)

@otto_mother.handle()
async def _ (bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent):
    #if not gunmu_checking_option:
    plain = event.message.extract_plain_text()
    _info(plain)

    if re.search(f"[{GUNMU_CHARS}]", plain):
        replaced = replace_gunmu(plain)
        _info("otto trigged.")
        if str(event.user_id) == "2257277732":
            await otto_mother.send(f"？你怎么只发了我是██啊，把话说完啊？")
        else:
            await otto_mother.send(f"？你怎么只发了 {replaced} 啊，把话说完啊？")
    else:
        _info("otto not trigged.")

    #else:
    #    _info("otto not trigged because option is false.")

"""