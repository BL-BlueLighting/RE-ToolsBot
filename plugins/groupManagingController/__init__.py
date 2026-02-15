import json
import logging
import random
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
from nonebot.adapters.onebot.v11 import Bot
import pytz
from apscheduler.triggers.interval import IntervalTrigger

from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot import require
import datetime

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

import plugins.userInfoController as dc
from toolsbot.configs import DATA_PATH
from toolsbot.services import _crit, _info, _warn

THIRTY_DAYS_BAN = 2591940 # 30 * 24 * 60 * 60
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
        user_info = await bot.call_api("get_stranger_info", user_id=int(qqNumber))
        res = res.replace("[QQ]", user_info["nick"])
    except Exception as e:
        _warn(f"Failed to get user info using qq number {qqNumber}. This is why:\n{e}")
        res = res.replace("[QQ]", "未知名称")

    return res

async def msg_reply(event: GroupMessageEvent) -> Union[int, None]:
    return event.reply.message_id if event.reply else None

# 获取本地时区
local_tz = pytz.timezone('Asia/Shanghai')

# 存储待验证用户
user_calcs: dict[str, dict] = {}
kicking_schedule_registered = False

# ============ 题目库 ============
MATH_QUESTIONS = [
    {
        "type": "math",
        "template": "{a} - (-{b}) = ?",
        "generate": lambda: {
            "a": random.randint(9, 99),
            "b": random.randint(99, 999),
        },
        "calculate": lambda data: data["a"] - (-data["b"])
    }
]

CHEMISTRY_QUESTIONS = [
    # 元素符号类
    {
        "type": "chem",
        "question": "Au 的元素符号对应什么元素？",
        "answer": "金",
        "aliases": ["gold", "金子", "au", "金元素"]
    },
    {
        "type": "chem",
        "question": "Fe 的元素名称是什么？",
        "answer": "铁",
        "aliases": ["iron", "铁元素", "fe"]
    },
    {
        "type": "chem",
        "question": "Ag 代表什么元素？",
        "answer": "银",
        "aliases": ["silver", "银子", "ag"]
    },
    {
        "type": "chem",
        "question": "Na 代表什么元素？",
        "answer": "钠",
        "aliases": ["钠元素", "sodium", "na"]
    },
    {
        "type": "chem",
        "question": "K 是什么元素的符号？",
        "answer": "钾",
        "aliases": ["钾元素", "potassium", "k"]
    },
    {
        "type": "chem",
        "question": "Cl 是什么元素的符号？",
        "answer": "氯",
        "aliases": ["氯元素", "chlorine", "cl"]
    },
    {
        "type": "chem",
        "question": "H 代表什么元素？",
        "answer": "氢",
        "aliases": ["氢元素", "hydrogen", "h"]
    },
    {
        "type": "chem",
        "question": "O 代表什么元素？",
        "answer": "氧",
        "aliases": ["氧元素", "oxygen", "o"]
    },
    {
        "type": "chem",
        "question": "C 是什么元素的符号？",
        "answer": "碳",
        "aliases": ["碳元素", "carbon", "c"]
    },
    {
        "type": "chem",
        "question": "N 代表什么元素？",
        "answer": "氮",
        "aliases": ["氮元素", "nitrogen", "n"]
    },
    {
        "type": "chem",
        "question": "Ca 是什么元素？",
        "answer": "钙",
        "aliases": ["钙元素", "calcium", "ca"]
    },
    {
        "type": "chem",
        "question": "原子序数为 1 的元素是什么？",
        "answer": "氢",
        "aliases": ["氢元素", "hydrogen", "h"]
    },
    {
        "type": "chem",
        "question": "原子序数为 6 的元素是什么？",
        "answer": "碳",
        "aliases": ["碳元素", "carbon", "c"]
    },
    {
        "type": "chem",
        "question": "原子序数为 8 的元素是什么？",
        "answer": "氧",
        "aliases": ["氧元素", "oxygen", "o"]
    },
    {
        "type": "chem",
        "question": "原子序数为 26 的元素是什么？",
        "answer": "铁",
        "aliases": ["铁元素", "iron", "fe"]
    },
    {
        "type": "chem",
        "question": "原子序数为 29 的元素是什么？",
        "answer": "铜",
        "aliases": ["铜元素", "copper", "cu"]
    },
    {
        "type": "chem",
        "question": "原子序数为 47 的元素是什么？",
        "answer": "银",
        "aliases": ["银元素", "silver", "ag"]
    },
    {
        "type": "chem",
        "question": "原子序数为 79 的元素是什么？",
        "answer": "金",
        "aliases": ["金元素", "gold", "au"]
    },
    
    # 化学式类
    {
        "type": "chem",
        "question": "水的化学式是什么？",
        "answer": "H2O",
        "aliases": ["h2o", "水", "water", "H₂O"]
    },
    {
        "type": "chem",
        "question": "二氧化碳的化学式是什么？",
        "answer": "CO2",
        "aliases": ["co2", "二氧化碳", "carbon dioxide"]
    },
    {
        "type": "chem",
        "question": "食盐（氯化钠）的化学式是什么？",
        "answer": "NaCl",
        "aliases": ["nacl", "氯化钠", "salt"]
    },
    {
        "type": "chem",
        "question": "甲烷的化学式是什么？",
        "answer": "CH4",
        "aliases": ["ch4", "甲烷", "methane"]
    },
    {
        "type": "chem",
        "question": "氨气的化学式是什么？",
        "answer": "NH3",
        "aliases": ["nh3", "氨气", "ammonia"]
    },
    {
        "type": "chem",
        "question": "硫酸的化学式是什么？",
        "answer": "H2SO4",
        "aliases": ["h2so4", "硫酸", "sulfuric acid"]
    },
    {
        "type": "chem",
        "question": "盐酸的化学式是什么？",
        "answer": "HCl",
        "aliases": ["hcl", "盐酸", "hydrochloric acid"]
    },
    {
        "type": "chem",
        "question": "氢氧化钠的化学式是什么？",
        "answer": "NaOH",
        "aliases": ["naoh", "氢氧化钠", "sodium hydroxide", "烧碱"]
    },
    {
        "type": "chem",
        "question": "乙醇的化学式是什么？",
        "answer": "C2H5OH",
        "aliases": ["c2h5oh", "酒精", "ethanol", "c₂h₅oh"]
    },
    {
        "type": "chem",
        "question": "葡萄糖的化学式是什么？",
        "answer": "C6H12O6",
        "aliases": ["c6h12o6", "葡萄糖", "glucose", "c₆h₁₂o₆"]
    },
    
    # 化学常识类
    {
        "type": "chem",
        "question": "空气中含量最多的气体是什么？",
        "answer": "氮气",
        "aliases": ["氮", "氮气", "n2", "nitrogen"]
    },
    {
        "type": "chem",
        "question": "酸碱度用什么符号表示？",
        "answer": "pH",
        "aliases": ["ph", "ph值", "酸碱度"]
    },
    {
        "type": "chem",
        "question": "最轻的气体是什么？",
        "answer": "氢气",
        "aliases": ["氢", "氢气", "h2", "hydrogen"]
    },
    {
        "type": "chem",
        "question": "植物光合作用需要的气体是什么？",
        "answer": "二氧化碳",
        "aliases": ["co2", "二氧化碳", "carbon dioxide"]
    },
    {
        "type": "chem",
        "question": "人体呼出的气体主要是什么？",
        "answer": "二氧化碳",
        "aliases": ["co2", "二氧化碳", "carbon dioxide"]
    },
    {
        "type": "chem",
        "question": "常用的灭火器中含有哪种气体？",
        "answer": "二氧化碳",
        "aliases": ["co2", "二氧化碳", "carbon dioxide"]
    },
    {
        "type": "chem",
        "question": "能使澄清石灰水变浑浊的气体是什么？",
        "answer": "二氧化碳",
        "aliases": ["co2", "二氧化碳", "carbon dioxide"]
    },
    {
        "type": "chem",
        "question": "铁生锈是发生了什么反应？",
        "answer": "氧化",
        "aliases": ["氧化反应", "氧化", "oxidation"]
    }
]

# 组合所有题目
ALL_QUESTIONS = MATH_QUESTIONS + CHEMISTRY_QUESTIONS

# ============ 定时任务 ============
async def welcome_kicking(bot: Bot):
    """检查并踢出超时未验证的用户"""
    joking_strs = [
        "一脚踹出本群",
        "请离本群", 
        "踹到银河系",
        "大运创飞",
        "发射到外太空",
        "送去火星",
        "踢去陪马斯克"
    ]
    
    to_remove = []
    
    for user_id, value in user_calcs.items():
        # 计算时间差
        time_diff = (datetime.datetime.now(local_tz) - value["time"]).total_seconds()
        
        if time_diff > 30:  # 超过30秒未验证
            try:
                await bot.call_api("set_group_kick", 
                                 group_id=value["group_id"], 
                                 user_id=value["user_id"])
                
                joke = random.choice(joking_strs)
                await bot.call_api("send_group_msg", 
                                 group_id=value["group_id"], 
                                 message=f"QQ 号为 {user_id} 的用户因超时未验证被{joke}")
                
                to_remove.append(user_id)
                print(f"已踢出超时用户 {user_id}")
                
            except Exception as e:
                print(f"踢出用户 {user_id} 失败: {e}")
    
    # 删除已处理的用户
    for user_id in to_remove:
        user_calcs.pop(user_id, None)


# ============ 入群通知事件 ============
welcomejoin_event = on_notice()

@welcomejoin_event.handle()
async def welcome(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    """新成员入群处理"""
    user = event.get_user_id()
    
    # 忽略机器人自身
    if user == bot.self_id:
        return
    
    # 检查管理员权限
    try:
        role_info = await bot.call_api("get_group_member_info", 
                                      group_id=event.group_id, 
                                      user_id=bot.self_id)
        role = role_info["role"]
        if role not in ["admin", "owner"]:
            await welcomejoin_event.finish("机器人不是管理员，无法进行验证")
    except Exception as e:
        print(f"获取角色信息失败: {e}")
        return
    
    # 发送欢迎消息
    try:
        await welcomejoin_event.send(f"欢迎新成员 {user} 入群！")
    except:
        pass
    
    # 随机选择一道题目
    question_data = random.choice(ALL_QUESTIONS)
    
    if question_data["type"] == "math":
        # 数学题
        params = question_data["generate"]()
        correct_answer = str(question_data["calculate"](params))
        question_text = question_data["template"].format(**params)
        
        user_calcs[user] = {
            "time": datetime.datetime.now(local_tz),
            "user_id": user,
            "group_id": event.group_id,
            "check": correct_answer,
            "type": "math",
            "question": question_text,
            "raw_answer": correct_answer
        }
        
        message = (
            f"🔢 TLoH Bot 数学验证\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"    - 请计算下面的表达式：\n"
            f"    - {question_text}\n\n"
            f"    - 请发送：^verify 你的答案\n"
            f"    - ⏱️ 你只有30秒时间"
        )
        
    else:
        # 化学题
        question = question_data["question"]
        correct_answer = question_data["answer"]
        aliases = question_data.get("aliases", [])
        
        user_calcs[user] = {
            "time": datetime.datetime.now(local_tz),
            "user_id": user,
            "group_id": event.group_id,
            "check": correct_answer,
            "aliases": aliases,
            "type": "chem",
            "question": question,
            "raw_answer": correct_answer
        }
        
        message = (
            f"🧪 TLoH Bot 化学验证\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"    - 请回答下面的化学问题：\n"
            f"    - {question}\n\n"
            f"    - 请发送：^verify 你的答案\n"
            f"    - ⏱️ 你只有30秒时间"
        )
    
    await welcomejoin_event.send(message)
    
    # 注册定时任务（如果尚未注册）
    global kicking_schedule_registered
    if not kicking_schedule_registered:
        try:
            from apscheduler.schedulers.asyncio import AsyncIOScheduler
            import nonebot
            
            scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler
            
            # 5秒后开始第一次检查，之后每10秒检查一次
            first_run = datetime.datetime.now(local_tz) + datetime.timedelta(seconds=5)
            
            scheduler.add_job(
                welcome_kicking,
                trigger=IntervalTrigger(seconds=10, start_date=first_run),
                args=(bot,),
                id="welcome_verify_kicker",
                misfire_grace_time=30,
                replace_existing=True
            )
            kicking_schedule_registered = True
            print("验证超时检查任务已注册")
            
        except Exception as e:
            print(f"注册定时任务失败: {e}")


# ============ 验证命令 ============
welcome_verify_event = on_command("verify", priority=10)

@welcome_verify_event.handle()
async def verify_handler(bot: Bot, event: GroupMessageEvent, 
                        state: T_State, cmd_arg: Message = CommandArg()):
    """处理验证答案"""
    user = str(event.user_id)
    
    # 检查用户是否在验证列表中
    if user not in user_calcs:
        await welcome_verify_event.finish("❌ 您不在验证队列中或已过期")
    
    user_data = user_calcs[user]
    user_answer = cmd_arg.extract_plain_text().strip().lower()
    
    print(f"用户 {user} 输入答案: {user_answer}")
    print(f"正确答案: {user_data['check']}")
    
    # 根据题目类型验证答案
    is_correct = False
    
    if user_data["type"] == "math":
        # 数学题验证（必须是数字）
        if user_answer.isdigit() and int(user_answer) == int(user_data["check"]):
            is_correct = True
    else:
        # 化学题验证（支持别名）
        correct = user_data["check"].lower()
        aliases = [a.lower() for a in user_data.get("aliases", [])]
        
        if user_answer == correct or user_answer in aliases:
            is_correct = True
    
    if is_correct:
        # 答案正确
        await welcome_verify_event.send("✅ 答案正确！欢迎入群！")
        user_calcs.pop(user, None)
        print(f"用户 {user} 验证通过")
    else:
        # 答案错误，踢出
        await welcome_verify_event.send("❌ 答案错误，你已被移出群聊")
        
        try:
            await bot.call_api("set_group_kick", 
                             group_id=user_data["group_id"], 
                             user_id=user)
            print(f"已踢出验证失败用户 {user}")
        except Exception as e:
            print(f"踢出用户 {user} 失败: {e}")
        
        user_calcs.pop(user, None)
        await welcome_verify_event.finish()

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
    await friend_add.finish("TLoH Bot GROUP MANAGING MODULE\n    - 已通过您的请求。")

undo_message = on_command("undo", permission=SUPERUSER, priority=5)

@undo_message.handle()
async def undo_msg(bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    # get reply id
    reply_id = await msg_reply(event)

    if reply_id == None:
        await undo_message.finish("TLoH Bot GROUP MANAGING MODULE\n    - 请回复一条消息再撤回")
    # delete msg
    try:
        await bot.call_api("delete_msg", message_id=reply_id)
    except ActionFailed as afd:
        _crit(f"Failed to undo message using msgid。This is why:\n{afd}")
        await undo_message.finish("TLoH Bot GROUP MANAGING MODULE\n    - 未能成功撤回消息。请确认消息存在或发送人不是管理\\群主\\bot自己（虽然会撤回但是还是会报错）")
    else:
        await undo_message.finish("TLoH Bot GROUP MANAGING MODULE\n    - 成功撤回消息 msg_id=" + str(reply_id) + "。") #type: ignore


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
            await mutesb.finish(f"TLoH Bot GROUP MANAGING MODULE\n    - 无法禁言该用户。该用户已被禁言或是管理员\\群主")

    await mutesb.finish(f"TLoH Bot GROUP MANAGING MODULE\n    - 已禁言 {sblist} {arg}。")

# unmutesb

unmute = on_command("unmute", permission=SUPERUSER)

@unmute.handle()
async def unmute_command(bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    sblist = At(event.json())

    arg = args.extract_plain_text()

    for qq in sblist:
        await bot.call_api("set_group_ban", group_id=event.group_id, user_id = qq, duration=0)

    await mutesb.finish(f"TLoH Bot GROUP MANAGING MODULE\n    - 已取消禁言 {sblist} {arg}。")

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
    result = await bot.call_api(api_name, **{
        k: v for k, v in (
            p.split("=", 1) for p in api_params if "=" in p
        )
    })

    # finish
    await call_api_command.finish("TLoH Bot GROUP MANAGING MODULE\n    - 已执行。\n    - 以下为具体内容：\n    - " + result.__str__())

# test admin permission
test_admin = on_command("testadmin", permission=SUPERUSER)

@test_admin.handle()
async def _ (bot: nonebot.adapters.onebot.v11.Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    # direct run onebot api
    admin_list = await bot.call_api("get_group_member_info", group_id=event.group_id, user_id=bot.self_id)
    await test_admin.finish(f"TLoH Bot GROUP MANAGING MODULE\n    - 该 Bot 在本群的权限是 {admin_list['role']}。")

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
