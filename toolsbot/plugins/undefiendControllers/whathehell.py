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

from nonebot.rule import to_me

import toolsbot.plugins.userInfoController as uic
from lxml import html as hi

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

"""
RE: ToolsBot
Tools Bot 的第二版。

@author: Latingtude

undefiendControllers.whathehell MODULE.
What the hell 什么魔鬼
"""

TITLE = "RE: ToolsBot"

hell_funny = on_command("hellfunny", priority=5, block=True)


@hell_funny.handle()
async def handle_hell_funny(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    # get today date
    today = datetime.datetime.now()
    _info(f"当前日期: {today.month}-{today.day}")  # 添加日期日志

    # if date = 9.11
    if today.month == 9 and today.day == 11:
        await hell_funny.finish("✈️    ⏸")

    # if date = 5.20
    if today.month == 5 and today.day == 20:
        await hell_funny.finish("祝有情人终成眷属，祝眷侣早日丧侣")

    # if date = 6.1
    if today.month == 6 and today.day == 1:
        await hell_funny.finish("祝小孩子们考0蛋")

    # if date = 9.1
    if today.month == 9 and today.day == 1:
        await hell_funny.finish("开学快乐")

    # if date = 11.29 / 11.30
    if (today.month == 11 and today.day == 29) or (today.month == 11 and today.day == 30):
        await hell_funny.finish("今天是地狱笑话模块被加入 ToolsBot 的日子，蝼蚁们，颤抖吧！！\n嘎啊哈哈哈哈")

    # if date = 12.24
    if today.month == 12 and today.day == 24:
        await hell_funny.finish("Bot 主生日快乐。")

    # if date = 12.31
    if today.month == 12 and today.day == 31:
        await hell_funny.finish("新年快乐！\n🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
