from nonebot import *
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import nonebot,random,json,requests
from nonebot.matcher import Matcher
from nonebot.params import EventMessage
from nonebot.adapters import Message
from time import sleep as wait
from random import uniform as wrd
import os, pathlib
from nonebot.adapters.onebot.v11.message import Message as v11message

"""
RE: ToolsBot
Tools Bot 的第二版。

@author: Latingtude 

mainController
"""

TITLE = "RE: ToolsBot"

"""
兜底函数
"""
# 获取配置里的 COMMAND_START，默认是 {'/', '!', '／', '！'}
command_starts = get_driver().config.command_start

def is_unmatched_command(msg: Message) -> bool:
    text = msg.extract_plain_text().strip()
    # 消息以 COMMAND_START 开头，并且不为空（避免只有 `/`）
    return bool(text) and any(text.startswith(s) for s in command_starts)

#fallback = on_message(priority=1000000, block=True)

#@fallback.handle()
async def _(msg: Message = EventMessage(), matcher: Matcher = Matcher()):
    if is_unmatched_command(msg):
        await matcher.finish("未知指令，请检查输入是否正确。")
        
"""
Help 函数
用于基本的介绍

@author: Latingtude
"""
help_function = on_command("help", aliases={"帮助"}, priority=10)

@help_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    msg = TITLE
    # 添加图片
    # 获得绝对路径
    await help_function.finish(v11message(f"[CQ:image,file=https://airoj.latingtude-studios.icu/helpdocument_new.png,id=400000]"))
    
"""
check 函数
检测 bot 是否存活

@author: Latingtude
"""

check_function = on_command("check", priority=10)

@check_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    await check_function.finish("RE: ToolsBot 还活着呢，没死。")
    
"""
^ping & ^pong 函数
和 bot 打乒乓球

@author: Latingtude
"""
ping_function = on_command("ping", priority=10)
pong_function = on_command("pong", priority=10)

@ping_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    # 随机
    if random.randint(1, 10) > 5:
        await check_function.finish("没接住")
    else:
        await check_function.finish("pong")

@pong_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    if random.randint(1, 10) > 5:
        await check_function.finish("没接住")
    else:
        await check_function.finish("ping")


"""
^essence 函数
设置精华消息

@author: Latingtude
"""
set_essence = on_command("essence", priority=5, permission=SUPERUSER)

@set_essence.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if event.reply:
        msg_id = event.reply.message_id
    else:
        await set_essence.finish("RE: ToolsBot Essence Set\n    - 请回复一条消息来设为精华")

    try:
        await bot.call_api("set_essence_msg", message_id=msg_id)
    except Exception as e:
        await set_essence.finish(f"RE: ToolsBot Essence Set\n    - 设置精华失败：{e}")
    else:
        await set_essence.finish("RE: ToolsBot Essence Set\n    - 已成功将该消息设为精华 ✨")


"""
goodsaying 函数

名言金句函數
@author: Latingtude
"""

goodsaying_function = on_command("goodsaying", priority=10)

@goodsaying_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " 名言金句"
    _msg = args.extract_plain_text()
    url = "https://hitokoto.152710.xyz"

    # request
    message = requests.get(url)

    # get json
    _jsonmessage = json.loads(message.content)

    # apppend
    hitokoto = _jsonmessage.get("hitokoto", "世上本沒有路，但是人走多了，便成了路。")
    _from = _jsonmessage.get("from", "《棍母》")
    creator = _jsonmessage.get("creator", "魯迅: 周樹人")

    # format
    msg += f"""
    {hitokoto}
                —— {_from} --- {creator}"""
    
    # finish
    await goodsaying_function.finish(msg)