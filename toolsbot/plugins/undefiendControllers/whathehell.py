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

"""
地狱笑话模块 

@author: Latingtude
"""
# catch all message after all commands
hell_funny = on_message(priority=10)

@hell_funny.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    # if not at bot, then return
    if bot.self_id not in uic.At(event.json()):
        return

    # get today date
    today = datetime.date.today()

    # if date = 9.11
    if today == datetime.date(datetime.date.today().year, 9, 11):
        # send message
        await hell_funny.finish("✈️    ⏸")

    # if date = 5.20
    if today == datetime.date(datetime.date.today().year, 5, 20):
        await hell_funny.finish("祝有情人终成眷侣，祝眷侣早日丧侣")

    # if date = 6.1
    if today == datetime.date(datetime.date.today().year, 6, 1):
        await hell_funny.finish("祝小孩子们考0蛋")

    # if date = 9.1
    if today == datetime.date(datetime.date.today().year, 9, 1):
        await hell_funny.finish("开学快乐")

    # if date = 11.29 / 11.30
    if today == datetime.date(datetime.date.today().year, 11, 29) or today == datetime.date(datetime.date.today().year, 11, 30):
        await hell_funny.finish("今天是地狱笑话模块被加入 ToolsBot 的日子，蝼蚁们，颤抖吧！！\n嘎啊哈哈哈哈")

    # if date = 12.31
    if today == datetime.date(datetime.date.today().year, 12, 31):
        await hell_funny.finish("新年快乐！\n🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")