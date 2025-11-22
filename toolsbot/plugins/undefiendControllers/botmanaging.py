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

undefiendControllers.botmanaging MODULE.
"""

stop_command = on_command("botstop", priority=5, permission=SUPERUSER)

@stop_command.handle()
async def stop_bot(event: MessageEvent):
    # 发送 msg 到 bot 加入的所有群聊
    msg = """RE: ToolsBot - 停机公告
    由于维护原因，RE: ToolsBot 将停止运行，直到 RE: ToolsBot 重新启动。
    """
    
    # get all group ids
    bot = nonebot.get_bot()
    group_list = await bot.get_group_list()
    
    for group in group_list:
        try:
            await bot.send_group_msg(group_id=group["group_id"], message=msg) 
        except ActionFailed as e:
            _warn(f"Failed to send stop message to group {group['group_id']}. This is why:\n{e}")
            
        # use native api
    
start_command = on_command("botstart", priority=5, permission=SUPERUSER)

@start_command.handle()
async def start_bot(event: MessageEvent):
    # 发送 msg 到 bot 加入的所有群聊
    msg = """RE: ToolsBot - 启动公告
    RE: ToolsBot 已重新启动。
    """

    # get all group ids
    bot = nonebot.get_bot()
    group_list = await bot.get_group_list()
    
    for group in group_list:
        try:
            await bot.send_group_msg(group_id=group["group_id"], message=msg) 
        except ActionFailed as e:
            _warn(f"Failed to send stop message to group {group['group_id']}. This is why:\n{e}")
            
        # use native api
    
