from nonebot import *
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import nonebot,random,json,requests
from time import sleep as wait
from random import uniform as wrd
import os
import datetime
import logging, re
from collections import Counter
from toolsbot.plugins.userInfoController import User

logging.basicConfig(
    filename='botlog.log',
    filemode='a',       
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# logging pointers
_info = logging.info
_warn = logging.warning
_erro = logging.error
_crit = logging.critical

# logging settings

"""
RE: ToolsBot
Tools Bot 的第二版。

@author: Latingtude 

undefiendControllers.echoManager
"""

TITLE = "RE: ToolsBot"

"""
echotadd 函数

添加关键词和文本，仅限 SUPERUSER.
@author: Latingtude
"""

echot_add_function = on_command("echotadd", aliases={"echoThingAdd"}, priority=10, permission=SUPERUSER)

@echot_add_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " - echoThing Managing"
    user = User(event.get_user_id())
    _msg = args.extract_plain_text()
    
    keyword = _msg.split(" ")[0]
    content = _msg.split(" ")[1:]
    
    keywords = json.load(open("./data/echoThings.json", "r", encoding="utf-8"))

    if keyword in keywords.keys():
        await echot_add_function.finish(msg + "\n    - 关键词：" + keyword + "\n    - 该项目已存在。")
    else:
        keywords[keyword] = " ".join(content)
        json.dump(keywords, open("./data/echoThings.json", "w", encoding="utf-8"))
        await echot_add_function.finish(msg + "\n    - 关键词：" + keyword + "\n    - 内容：\n    " + " ".join(content))
    
"""
echotdel 函数

删除关键词和文本，仅限 SUPERUSER.
"""
    
"""
echot 函数

输出关键词指定的文本
@author: Latingtude
"""

echot_function = on_command("echot", aliases = {"echoThing"},priority=10)

@echot_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " - echoThing"
    user = User(event.get_user_id())
    _msg = args.extract_plain_text()
    
    # read echoT.json
    keywords = json.load(open("./data/echoThings.json", "r", encoding="utf-8"))
    
    if _msg in keywords.keys():
        await echot_function.finish(msg + "\n    - 关键词：" + _msg + "\n    - 内容：\n    " + keywords[_msg])
    else:
        await echot_function.finish("未找到关键词，请检查是否拼写正确。")