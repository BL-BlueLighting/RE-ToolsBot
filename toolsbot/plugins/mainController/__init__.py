from nonebot import *
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import nonebot,random,json,requests
from time import sleep as wait
from random import uniform as wrd
import os

"""
RE: ToolsBot
Tools Bot 的第二版。

@author: Latingtude 

mainController
"""

TITLE = "RE: ToolsBot"

"""
Help 函数
用于基本的介绍

@author: Latingtude
"""
help_function = on_command("help", aliases={"帮助"}, priority=10)

@help_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    msg = TITLE
    msg += """ 帮助
普通用户可用：
    ^help: 显示 RE: ToolsBot 的帮助
    ^info [(可选) @用户]: 查看信息
    ^morning: 签到，早上好！
    ^buy: 购买 / 使用物品
    ^b(ase) [64/32/16/85/58]: Base XX 编码解码
    ^lc64: 凉菜 64 编码解码
    ^ai [内容]: 使用 AI 功能，1 token = 1 积分
    ^usecode [code]: 兑换码，可以找 bot 主要（前提是他给）
    ^pay [@人] [数量]: 转账，适用于给钱或者换号的情况
    ^echo [内容]: 输出内容，请不要输出违反 QQ 规则的内容，很容易风控的
    ^cleanwaste: 捡 垃 圾
    ^moneybest: 排行榜 前 10
    ^question: 弱智吧问题随机
    ^ping: 打  乓
    ^pong: 乒  球
    ^aes: 加密解密 AES
    ^accountStatus: 查看当前账户状态
    ^check: Bot 你还活着吗？？
    ^banlist: 封禁列表
    ^redpacket: 发红包
    ^openredpacket: 抢红包
    ^mcserver: 查询 MC 服务器状态，使用 ^mcserver 来获得使用方法。
    ^modifyname: 修改用户昵称（好像这玩意之前一直都没写）

超级用户可用：
    ^ban pardon: 封禁 解除封禁 （仅超级用户）
    ^mute ^unmute [ats] minute=[分钟]: 禁言（请把 minute 放在最后面，unmute 不需要 minute）
    ^undo [回复一条消息]: 撤回消息
    ^call_api [API 名] [params]=[value]: 使用 OneBot V11 API。
    ^essence: 设置精华消息（需回复该条消息）
    
FiNALE SCOPE - 终末之盒:
    ^finaleScope: 查询目前所有的门数量和你已经解锁的门。
    ^finaleScopeNext: 解锁下一个你可以解锁的门。

METAEvent & Notice：
    Welcome: 新人入群欢迎，赠送 50 积分
    Escape: 人员离开消息
    FriendAdd: 好友申请自动同意
"""
    await help_function.finish(msg)
    
"""
check 函数
检测 bot 是否存活

@author: Latingtude
"""

check_function = on_command("check", aliases={""}, priority=10)

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
    await check_function.finish("pong")

@pong_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
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