import logging

import requests
from lxml import html as hi
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent,
                                         PrivateMessageEvent)
from nonebot.params import CommandArg

import plugins.userInfoController as uic

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

undefiendControllers.scpfoundation MODULE.
SCP 基金会相关功能。
"""

TITLE = "RE: ToolsBot"

"""
SCP 函数

@author: Latingtude
"""

scp_function = on_command("scp", aliases={""}, priority=10)

@scp_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, _args: Message = CommandArg()):
    msg =  TITLE + " - SCP 基金会相关功能"
    user = uic.User(event.get_user_id())
    _msg = _args.extract_plain_text()
    args = _msg.strip().split(" ")

    # SCP FOUNDATION IS FOR EVERYONE.

    if len(args) == 0:
        msg += "\n    Welcome to S.C.P. Foundation."
        msg += "\n    You can use commands under:"
        msg += "\n        - ^scp doc(document) [document id] [branch=en]"
        msg += "\n    Now supports branches under:"
        msg += "\n        - China (cn)"
        msg += "\n        - English (en)"
        msg += "\n        - Minecraft (mc)"
        msg += "\n        - Cloud (cloud)"
        await scp_function.finish(msg)

    elif args [0] == "doc" or args [0] == "document":
        # fetch scp website
        branch = "en"

        if len(args) == 1:
            msg += "    - 请输入文档编号。"
            await scp_function.finish(msg)

        if len(args) == 2:
            branch = "en"
        else:
            supportBranches = ["cn", "en", "mc", "cloud"]
            # 中分，主站，麦分，云分
            if args [2].lower() in supportBranches:
                branch = args [2].lower()
            else:
                branch = "en"
                msg += "    - 您所要检索的分支目前 RE: ToolsBot 不支持。\n    - 将默认使用 EN 编号查找。"

        msg += f"\n    - 检索 SCP-{branch}-{args [1]}"

        global scpurl
        scpurl = ""

        if branch == "cn":
            scpurl = f"https://scp-wiki-cn.wikidot.com/scp-cn-{args [1]}"
        elif branch == "en":
            scpurl = f"https://scp-wiki.wikidot.com/scp-{args [1]}"
        elif branch == "mc":
            scpurl = f"https://scp-wiki-mc.wikidot.com/scp-mc-{args [1]}"
        elif branch == "cloud":
            scpurl = f"https://scp-wiki-cloud.wikidot.com/scp-cloud-{args [1]}"

        # get page content
        try:
            page = requests.get(scpurl).content.decode("gbk")
            level = "safe"

            if "euclid" in page or "Euclid" in page:
                level = "euclid"
            elif "keter" in page or "Keter" in page:
                level = "keter"

            _info(page)

            page = hi.fromstring(page)

            msg += f"\n    - 检索成功。"
            msg += f"\n    - SCP 文档信息："
            msg += f"\n        - 编号：SCP-{branch}-{args [1]}"
            msg += f"\n        - 等级：{level}"
            # get rate from class 'number'
            msg += f"\n        - Rate: {page.xpath('//div[@class="number"]/text()')[0]}"
            msg += f"\n        - 链接：{scpurl}"
        except Exception as e:
            msg += "\n    - 处理过程出现问题。"
            _erro(e.__str__())
            await scp_function.finish(msg)

        await scp_function.finish(msg)
