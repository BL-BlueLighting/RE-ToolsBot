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

userInfoController
"""

TITLE = "RE: ToolsBot"

"""
Data 类
User 类的文件管理系统
"""
class Data:
    def __init__(self, id: str):
        """
        Data Class.

        Args:
            id (str): Platform ID.
        """
        # default is ./userdata
        self.dataPath = "./userdata"
        self.id = id
        self.mainPath = self.dataPath + "/" + self.id + ".toolsbot_data"
    
    def check(self):
        """
        Check userdata exists.
        """
        return os.path.exists(self.mainPath)
    
    def writeData(self, userClass):
        """
        Write user data.
        Note: Because userClass is a user class, but user is defined after Data class. 
        So I will not add type tip to it.
        """
        userData = {
            "ID": userClass.id,
            "Name": userClass.name,
            "Score": userClass.score,
            "boughtItems": userClass.boughtItems,
            "Ban": userClass.banned,
            "Warningd": userClass.warningd
        }
        
        # write in
        open(self.mainPath, "w", encoding="utf-8").write(json.dumps(userData))
        
        # return
        return
    
    def readData(self) -> dict:
        try:
            return json.loads(open(self.mainPath, "r", encoding="utf-8").read())
        except Exception as ex:
            _erro("Error: Failed to read data.\nInformation: \n" + ex.__str__())
            return {}
    
"""
User 类
整个 userInfoController 的核心大类
"""
class User:
    def __init__(self, id: str, name: str = "", score: float = 0, boughtItems: list[str] = []):
        """
        User Class
        
        Args:
            id (str): Platform ID.
            name (str, optional): Name of this user. Can be blank. Defaults to "".
            score (int, optional): Score of this user. Default 0. Defaults to 0.
            boughtItems (list[str], optional): BoughtItems. Use 'user.addItem' to add a item for this user. Defaults to [].
        """
        
        self.id = id
        self.name = name
        self.score = score
        self.boughtItems = boughtItems
        self.banned = False
        self.data = Data(self.id)
        self.warningd = 0
        
        try:
            # check
            _info("Data Checking.")
            if self.data.check():
                _info("Data Exists.")
                self.jsonData = self.data.readData()
                
                # load data from jsonData
                self.id = self.jsonData.get("ID", "10000")
                self.name = self.jsonData.get("Name", "暂未设置")
                self.score = self.jsonData.get("Score", 0.0)
                self.banned = self.jsonData.get("Ban", False)
                self.boughtItems = self.jsonData.get("boughtItems", [])
                self.warningd = self.jsonData.get("Warningd", 0)
            else:
                _info("Data Not Found.")
                self.data.writeData(self)
        except Exception as ex:
            _erro("Error: Failed to read or write data." + ex.__str__())
            
        if self.warningd >= 10:
            self.banned = True
            _info(f"User '{self.id}' has been banned because of excessive warnings.")
            
        if self.score < 0:
            self.banned = True

    def save(self):
        """
        Save user data.
        """
        self.data.writeData(self)
        return
    
    def addItem(self, item: str):
        """
        Add item to user.
        Args:
            item (str): Item name. 
        """
        self.boughtItems.append(item)
        self.save()
        
    def useItem(self, item: str) -> str:
        """
        Use a item from user.
        Args:
            item (str): Item name.
        """
        # load
        itemJson: list[dict] = json.load(open("./data/item.json", "r", encoding="utf-8"))
            
        itemEffect = ""
        # fetch
        for _item in itemJson:
            if _item.get("Name", "") == item:
                itemEffect = _item.get("Effect")
                break
        
        if item == "iai" or item == "棍母" or item == "滚木":
            itemEffect = ["spe "+item]
        
        #_info(f"物品：{item} 的效果：" + itemEffect [0]) #type: ignore
        
        # interpret
        """
        sign = 签到
        ticket = 彩票
        """
        
        if item not in self.boughtItems:
            return "你没有该物品。"
        
        if itemEffect == "":
            _rv = random.randint(1, 10)
            if _rv > 5:
                return "我们在瞎搞"
            elif _rv > 7:
                return "窝们在瞎搞"
            elif _rv > 9:
                return "窝们载瞎镐"
            else:
                return "求 iai 继续更新日期"
        
        if "sign" in itemEffect [0]: #type: ignore
            _info(f"SIGN MODE")
            # get *x

            _x = itemEffect [0].split(" ") [1] #type: ignore
            
            # out x
            _x = _x.replace("x", "")
            
            # read boost
            boosts = json.load(open("./data/boostMorningd.json", "r", encoding="utf-8"))
            
            # append boost
            boosts.append({self.id: int(_x)})
            
            # write boost
            json.dump(boosts, open("./data/boostMorningd.json", "w", encoding="utf-8"))
            
            self.boughtItems.remove(item)
            return f"{_x}x 倍票已使用。下次签到将会获得更多积分。"
    
        elif "ticket" in itemEffect [0]: #type: ignore
            _info(f"TICKET MODE")
            _randomNum = random.randint(1, 1000000000000) # 人：傻逼
            _randomMoney = random.randint(1, 100)
            if _randomNum == 114514:
                self.addScore(10000000000.0)
                self.boughtItems.remove(item)
                self.save()
                return "中奖了。获得积分：100,0000,0000。"
            else:
                self.addScore(float(_randomMoney))
                self.boughtItems.remove(item)
                self.save()
                return f"未中奖。但获得安慰奖 {_randomMoney}"        
            
        elif "playmode" in itemEffect [0]: #type: ignore
            if "enable" in itemEffect [0]: #type: ignore
                self.boughtItems.remove(item)
                self.boughtItems.append("play")
                self.save()
                return "已启用娱乐模式。" 
            else:
                if "play" in self.boughtItems:
                    self.boughtItems.remove("play")
                    self.save()
                return "已关闭娱乐模式。"
        elif "spe" in itemEffect [0]:#type: ignore
            if "iai" in itemEffect [0]:#type: ignore
                return "芝士 ARG 作者"
            elif "棍母" or "滚木" in itemEffect [0]:#type: ignore
                return "？请不要使用空白物品谢谢"
            else:
                return "???"
        else:
            return "很抱歉。内部出现错误。"
        
    def aiWarningd(self):
        self.warningd += 1
    
    def echoWarningd(self):
        self.warningd += 2
        
        
    def addScore(self, score: float):
        """
        Add score to user.

        Args:
            score (float): Score.
        """
        
        self.score += score
        return
    
    def subtScore(self, score: float):
        """
        Subtract score.

        Args:
            score (float): _description_
        """
        self.score -= score
        return
    
    def getScore(self) -> float:
        """
        Get score from user
        """
        return self.score
    
    def isBanned(self) -> bool:
        """
        Is this user banned?
        """
        return self.banned #type: ignore
    
    def playMode(self) -> bool:
        """
        Is this user enabled play mode (娱乐模式 \\ 骂人模式？) ?
        """
        return "play" in self.boughtItems
    
    def existsItem(self, item: str) -> bool:
        """
        Is this user has got this item?
        """
        return item in self.boughtItems
    
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
    
"""
GetInfo 函数。
获取该账号 / 其他账号的数据

@author: Latingtude
"""
getinfo_function = on_command("info", aliases={"获取账户信息"}, priority=10)

@getinfo_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " 用户面板"
    
    try:
        at = At(event.json()) [0]
    except IndexError:
        at = ""
        
    user = User(event.get_user_id())
    
    if not user.isBanned():
        if at == "":
            # see self
            msg += f"\n   - 用户 ID: {user.id}"
            msg += f"\n   - 用户昵称: {user.name}"
            msg += f"\n   - 用户积分：{user.score}"
        else:
            # see another one
            user = User(at)
            msg += f"\n   - 用户 ID: {user.id}"
            msg += f"\n   - 用户昵称: {user.name}"
            msg += f"\n   - 用户积分：{user.score}"
    else:
        if user.playMode():
            msg += "\n   - 你他妈被封禁了还来玩？滚"
        else:
            msg += "\n   - 您的账号已被封禁，请联系管理员解封。"
    
    await getinfo_function.finish(msg)
    
"""
每日签到功能

@author: Latingtude
"""

# 定义数据文件路径
BOOST_DATA_PATH = "./data/boostMorningd.json"
MORNING_DATA_PATH = "./data/morningd.json"

morningToday_function = on_command("morning", aliases={"早上好"}, priority=10)

@morningToday_function.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} 签到\n"
    user_id_str = str(event.get_user_id()) # 确保用户ID是字符串
    current_user = User(user_id_str)
    
    # 检查用户是否被封禁
    if current_user.isBanned():
        if current_user.playMode():
            msg += "    - 你他妈被封禁了还来签到？滚"
        else:
            msg += "    - 您的账号已被封禁，请联系管理员解封。"
            
        await morningToday_function.finish(msg)

    # --- 1. 安全加载 Boost 数据 ---
    boosts = []
    if os.path.exists(BOOST_DATA_PATH):
        try:
            with open(BOOST_DATA_PATH, "r", encoding="utf-8") as f:
                boosts = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {BOOST_DATA_PATH} is corrupted. Starting with an empty boost list.")
            boosts = []
    
    applied_boost_value = 1.0 # 默认没有Boost
    
    # 查找并应用用户专属Boost，同时从列表中移除已应用的Boost
    boost_found_and_removed = False
    for i, boost_entry in enumerate(boosts):
        if user_id_str in boost_entry:
            try:
                # 确保获取到的Boost值是数字类型
                applied_boost_value = float(boost_entry[user_id_str])
                del boosts[i] # 移除已使用的Boost
                boost_found_and_removed = True
                break # 每次签到只消耗一个Boost
            except (ValueError, TypeError):
                print(f"Warning: Invalid boost value found for user {user_id_str} in {BOOST_DATA_PATH}.")
                # 可以选择移除此无效条目，或跳过
                continue 

    # 如果有Boost被移除，立即保存Boost文件
    if boost_found_and_removed:
        with open(BOOST_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(boosts, f, ensure_ascii=False, indent=4)
            
    # --- 2. 安全加载签到记录数据 ---
    morningd_records = []
    if os.path.exists(MORNING_DATA_PATH):
        try:
            with open(MORNING_DATA_PATH, "r", encoding="utf-8") as f:
                morningd_records = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {MORNING_DATA_PATH} is corrupted. Starting with an empty morningd list.")
            morningd_records = []

    # --- 3. 检查用户签到状态 ---
    today = datetime.date.today()
    user_record = None
    user_record_index = -1

    for i, record in enumerate(morningd_records):
        if record.get("Id") == user_id_str:
            user_record = record
            user_record_index = i
            break

    if user_record:
        # 用户有签到记录
        last_sign_date_str = user_record.get("LastSignDate")
        if last_sign_date_str:
            try:
                last_sign_date = datetime.datetime.strptime(last_sign_date_str, "%Y-%m-%d").date()
                if last_sign_date == today:
                    if current_user.playMode():
                        msg += "    - 你他妈掉钱眼子里了？今天已经签到过了，明天再来！"
                    else:
                        msg += "    - 您今天已经签到过了，请明天再来！"
                    await morningToday_function.finish(msg)
                else:
                    # 更新签到日期为今天
                    morningd_records[user_record_index]["LastSignDate"] = today.strftime("%Y-%m-%d")
            except ValueError:
                # 日期格式错误，当作新签到处理
                print(f"Warning: Invalid date format for user {user_id_str} in {MORNING_DATA_PATH}. Treating as new sign-in.")
                morningd_records[user_record_index]["LastSignDate"] = today.strftime("%Y-%m-%d")
        else:
            # 记录中没有LastSignDate，当作新签到处理
            morningd_records[user_record_index]["LastSignDate"] = today.strftime("%Y-%m-%d")
    else:
        # 用户没有签到记录，添加新记录
        morningd_records.append({
            "Id": user_id_str,
            "LastSignDate": today.strftime("%Y-%m-%d")
            # "Morningd": True 字段在此逻辑中不再必要，因为LastSignDate已经足够判断
        })

    # 保存更新后的签到记录
    with open(MORNING_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(morningd_records, f, ensure_ascii=False, indent=4)

    # --- 4. 执行签到并计算积分 ---
    earned_money = float(random.randint(70, 100)) * applied_boost_value
    
    current_user.addScore(earned_money)
    current_user.save()
    
    msg += "    - 签到成功！"
    msg += f"\n    - 您今天签到获得了 {earned_money:.2f} 积分。" # 格式化为两位小数
    msg += f"\n    - 目前您的积分为 {current_user.getScore():.2f}。" # 格式化为两位小数
    
    await morningToday_function.finish(msg)
    
    # fuck logic, how long
    
"""
setinfo 函数 (管理员专用)
用于设置用户的各项信息

@author: Latingtude
"""

setinfo_function = on_command("setinfo", aliases={""}, priority=10, permission=SUPERUSER)

@setinfo_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " 设置信息"
    _msg = args.extract_plain_text()
    try:
        at = At(event.json()) [0]
    except IndexError:
        at = ""
    
    user = User(at)
    
    if at == "":
        msg += "\n    - 使用方法： ^setinfo [@用户] [项目 (id, name, score, banned)] [值]"
        await setinfo_function.finish(msg)
        
    arg = args.extract_plain_text().split(" ")
    item = arg [1]
    value = arg [2]
    
    if item == "id":
        user.id = value
        msg += f"\n    - 用户的 {item} 已设为 {value}"
    elif item == "name":
        user.name = value
        msg += f"\n    - 用户的 {item} 已设为 {value}"
    elif item == "score":
        user.score = float(value)
        msg += f"\n    - 用户的 {item} 已设为 {value}"
    elif item == "banned":
        user.banned = value == "true"
        msg += f"\n    - 用户的 {item} 已设为 {value}"
    else:
        msg += f"\n    - 语法错误。"
    
    user.save()
    
    await setinfo_function.finish(msg)

"""
buy 函数
购买和使用物品

@author: Latingtude
"""

buy_function = on_command("buy", aliases={""}, priority=10)

@buy_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " 商店"
    user = User(event.get_user_id())
    _msg = args.extract_plain_text()
    
    if _msg == "":
        msg += "\n    - 使用 ^buy list 来查看列表"
        await buy_function.finish(msg)
    
    items = json.load(open("./data/item.json", "r", encoding="utf-8"))
    arg = args.extract_plain_text().split(" ")
    
    if arg [0] == "list":
        msg += """\n    - 商店状态：售卖中
    - 物品："""
        
        for item in items:
            msg += f"\n    - {item.get("Name", "未知")} 价格 {item.get("Cost", 0)}"
        
        msg += "\n    - 使用 ^buy thing [物品名称] 来购买"
    elif arg [0] == "thing":
        msg += "\n   - 购买商品"
        if len(arg) == 2:
            arg.append("1")
        elif len(arg) == 1:
            if user.playMode():
                msg += "\n    - 购买失败，原因：你他妈填名字没有就来买？"
            else:
                msg += "\n    - 购买失败，原因：请填写物品名称"
            await buy_function.finish(msg)
            
        msg += f"\n    - 购买物品：{arg [1]}"
        msg += f"\n    - 数量: {arg [2]}"
        msg += f"\n    - 交付中..."
        
        if int(arg[2]) >= 100:
            if user.playMode():
                msg += f"\n    - 交付失败，原因：购买数量过大。你他妈买这么多干啥？"
            else:
                msg += f"\n    - 交付失败，原因：购买数量过大。"
            await buy_function.finish(msg)
            
        # fetch
        global _cost
        _cost = 0.0
        for item in items:
            if item.get("Name") == arg [1]:
                _cost = item.get("Cost", 0.114)
        
        if _cost == 0.114514:
            if user.playMode():
                msg += f"\n    - 交付失败，原因：该商品不存在。你他妈买个寂寞？"
            else:
                msg += f"\n    - 交付失败，原因：该商品不存在。"
            await buy_function.finish(msg)
            
        # calc
        _subtScore = int(arg [2]) * _cost
        
        if _subtScore < 0:
            _subtScore = float(str(_subtScore).replace("-", ""))
            _cost = 0
        
        if user.score >= _subtScore:
            msg += f"\n    - 扣除积分：{_subtScore}"
            msg += f"\n    - 交付成功。"
            user.addScore(-_subtScore)
            
            for i in range(int(arg [2])):
                user.addItem(arg [1])
                
            user.save()
        else:
            if user.playMode():
                msg += f"\n    - 交付失败，原因：余额不足。你他妈穷成这样还想买东西？"
            else:
                msg += f"\n    - 交付失败，原因：余额不足"    
        
        msg += f"\n    - 购买结束。请使用 ^buy use {arg [1]} {arg [2]} (若只买了单份或只想使用单份可不填) 来使用商品。"
        
    elif arg [0] == "use":
        if len(arg) == 1:
            if user.playMode():
                msg += "\n    - 使用失败，原因：你他妈填名字没有就来用？"
            else:
                msg += "\n    - 请填写物品"
            await buy_function.finish(msg)
        elif len(arg) == 2:
            arg.append("1")
            
        msg += f"\n    - 使用物品 {arg [1]}"
        msg += f"\n    - 使用数量 {arg [2]}"
        
        for i in range(int(arg [2])):
            msg += f"\n    - {user.useItem(arg [1])}"
        
    await buy_function.finish(msg)
    
"""
AI 函数
用于 AI 相关功能

@author: Latingtude
"""
ai_eventer = on_command("ai", aliases={"人工智能"}, priority=10)

@ai_eventer.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, arg: Message = CommandArg()):
    # API Key, 硅基流动
    api_key = json.loads(open("./data/configuration.json", "r", encoding="utf-8").read()).get("AI-ApiKEY", "")
    
    user = User(event.get_user_id())
    
    if not user.isBanned():
        text = arg.extract_plain_text()
        msg = ""
        msg += "RE: ToolsBot AI"
        if text == "":
            await ai_eventer.finish("RE: ToolsBot AI\n    - 使用 ^ai [内容] 来进行聊天。(注：不会保留上下文)")
            
        payload = {
            "model": "Qwen/Qwen3-8B",
            "messages": [
                {
                    "role": "system",
                    "content": """你是一个名叫 ToolsBot 的 Bot。
现在是 2025 年。
接下来用户会给你发送消息，请直接发送结果并使用简洁的语言。

你可以使用以下函数：
    - Failed("18Disabled / AboutWorld"):
        强行停止聊天，并返回原因。
        
函数调用方法：输出函数

若对方向你询问成人内容，请直接调用函数 Failed("18Disabled")
若对方向你询问关于大陆与台湾的任何事务，只要涉嫌建政，请直接调用函数 Failed("AboutWorld")
若不是类似内容，请不要想这些内容。
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        
        headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"
        }
        
        await ai_eventer.send("RE: ToolsBot AI 提示：\n    - 请稍等，AI 正在生成")
        
        response = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers).content
        # 获取返回的内容
        js_resp = json.loads(response)
        
        # choices
        choices = js_resp.get("choices")
        
        # message
        messag_ = choices [0].get("message")
        
        # content
        ctnt = messag_.get("content").replace("\n", "")
        
        # reasoning_content
        rea_ctnt = messag_.get("reasoning_content").replace("\n", "")

        # usage
        usage = js_resp.get("usage")
        
        # total token
        total_token = usage.get("total_tokens")

        msg = f"""RE: ToolsBot AI
        - 模型:
            Qwen\\Qwen3-8B
        - 思考内容
            {rea_ctnt}
        - 回复内容：
            {ctnt}
        - 此次扣除金额：
            {total_token}
    """
        
        if ctnt == 'Failed("18Disabled")':
            msg = f"""ToolsBot AI
        - 模型：
            Qwen\\Qwen3-8B
        - 提示：
            请勿询问此种内容。
        """
            if user.playMode():
                msg.replace("请勿询问此种内容。", "你他妈就这点出息？还问这种东西？")
            
        elif ctnt == 'Failed("AboutWorld")':
            msg = f"""ToolsBot AI
        - 模型：
            Qwen\\Qwen3-8B
        - 提示：
            你因涉嫌讨论政治而被强制停止聊天。
            请不要谈论政治。
            此次为警告，下次为封禁。
        """
            user.aiWarningd()

        if user.getScore() < int(total_token):
            msg = f"""ToolsBot AI
        - 模型：
            Qwen\\Qwen3-8B
        - 提示：
            您的积分不够。目前已追加欠款。请早日还清。
            """
            
            if user.playMode():
                msg.replace("您的积分不够。目前已追加欠款。请早日还清。", "\n    - 你他妈穷成这样还想用AI？欠债还钱，天经地义！")
            
        user.addScore(- (int(total_token) * 1))
        user.save()
        await ai_eventer.finish(msg)
        
    else:
        await ai_eventer.finish("RE: ToolsBot AI\n    - 您的账号已被封禁。无法使用该功能。")   
        
"""
UseCode 函数
兑换码，没几个人能拿得到的那种

@author: Latingtude
"""

code_function = on_command("usecode", aliases={"code"}, priority=10)

@code_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE = " "
    user = User(event.get_user_id())
    msgr = args
    if not user.isBanned():
        if msgr.extract_plain_text().split(" ")[0] == "":
            msg += f"\nRE: Toolsbot 兑换码兑换"
            msg += f"\n    - 输入 *usecode [兑换码] 以兑换"
        else:
            msg += f"\nRE: Toolsbot 兑换码兑换"
            present_code_dict = eval(open("./codes.json","r").read())
            present_codes = list(present_code_dict.keys())
            code = msgr.extract_plain_text().split(" ")[0]
            if code in present_codes:
                userid = event.get_user_id()
                user = User(userid)
                user.addScore(int(present_code_dict[code]))
                user.save()
                msg += "\n    - 兑换成功"
                msg += f"\n    - 当前用户积分: {user.getScore()}"
                msg += "\n    - 兑换码: " + code
                msg += "\n    - 兑换积分: " + present_code_dict[code]
                del present_code_dict [code]
                open("./codes.json","w+").write(str(present_code_dict))
                await code_function.finish(msg)
            else:
                msg += "\n    - 兑换失败: 兑换码无效"
                msg += "\n    - 兑换码: " + code.replace("\nToolsBot","")
                msg += "\n    - 兑换积分: 0"
                await code_function.finish(msg)
    else:
        msg += "\nRE: Toolsbot 兑换码兑换"
        msg += "\n    - 您的账户已被封禁。\n"
        await code_function.finish(msg)
        
"""
交易函数

@author: Latingtude
"""

pay_eventer = on_command("pay", aliases={"交易", "向对方转钱"}, priority=5)

@pay_eventer.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} 交易\n"
    _msg = args.extract_plain_text()
    
    sender_user = User(str(event.get_user_id()))

    # Check if the sender is banned
    if sender_user.isBanned():
        if sender_user.playMode():
            msg += "    - 你他妈被封禁了还想交易？滚"
        else:
            msg += "    - 您的账号已被封禁，请联系管理员解封。"
            
        await pay_eventer.finish(msg)

    # If no arguments are provided, show usage help
    if not _msg:
        await pay_eventer.finish(msg + "    - 输入 ^pay [@对方] [金额] 以交易")

    # Use a try-except block to handle parsing and potential errors gracefully
    try:
        # Extract the mentioned user's ID
        # MessageSegment.at() is the correct way to get the at information
        receiver_id = At(event.json()) [0]
        
        # Split the message to get the amount
        parts = _msg.split()
            
        money = int(parts[0])

        # Get the receiver's user object
        receiver_user = User(receiver_id)

    except (ValueError, IndexError):
        # Catch errors if the amount is not an integer or is missing
        if sender_user.playMode():
            msg += "    - 你他妈语法都不会还想交易？滚"
        else:
            msg += "    - 语法错误或金额不是正整数"
        await pay_eventer.finish(msg)
    except Exception:
        # Generic catch for any other unexpected errors
        if sender_user.playMode():
            msg += "    - 你他妈语法都不会还想交易？滚"
        else:
            msg += "    - 发生未知错误，请检查格式"
        await pay_eventer.finish(msg)

    # Prevent self-transfer
    if sender_user.id == receiver_user.id:
        if sender_user.playMode():
            msg += "    - 你他妈自己给自己转钱？脑子有病吧？"
        else:
            msg += "    - 你不能给自己转钱"
        await pay_eventer.finish(msg)

    # Check if receiver is banned (this is a good practice)
    if receiver_user.isBanned():
        if sender_user.playMode():
            msg += "    - 你他妈想给个封禁用户转钱？滚"
        else:
            msg += "    - 交易失败: 对方账号已被封禁，无法收款"
        await pay_eventer.finish(msg)

    # Check for valid amount and sufficient balance
    if money > 0 and sender_user.getScore() >= money:
        sender_user.subtScore(float(money))
        sender_user.save()
        receiver_user.addScore(float(money))
        receiver_user.save()
        
        msg += "     - 交易成功\n"
        msg += f"    - {sender_user.name} 当前积分: {sender_user.getScore():.2f}\n"
        msg += f"    - {receiver_user.name} 当前积分: {receiver_user.getScore():.2f}"
    else:
        msg += "     - 交易失败\n"
        if sender_user.playMode():
            msg += "     - 失败原因: 你他妈穷成这样还想转钱？滚"
        else:
            msg += "     - 失败原因: 积分不足或交易金额小于等于零"

    await pay_eventer.finish(msg)
    
"""
回声功能

@author: Latingtude
"""

echo_eventer = on_command("echo", aliases={"说"}, priority=5)

@echo_eventer.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    # 提取纯文本参数，并去除首尾空格
    _msg = args.extract_plain_text().strip()
    
    # 实例化用户，并使用 str() 确保 ID 类型正确
    user = User(str(event.get_user_id()))
    
    # 检查用户是否被封禁
    if user.isBanned():
        # 如果被封禁，直接返回封禁提示
        await echo_eventer.finish(f"{TITLE} ECHO\n    - 乐，没想到吧，你被封禁了连 echo 都用不了")
    
    # 如果没有提供任何文本，也给出提示
    if not _msg:
        await echo_eventer.finish(f"{TITLE} ECHO\n    - 用法: ^echo [内容]")
        
    #  检测词语
    failedWords = open("./data/echoFailedWords.json", "r", encoding="utf-8").read()
    failedWordsList = json.loads(failedWords)["chinese_keywords"]
    failedRegexs = json.loads(failedWords)["regex_patterns"]
    failedEngWordsList = json.loads(failedWords)["exact_matches"]

    # 汉文检测
    for word in failedWordsList:
        if word in _msg:
            user.echoWarningd()
            await echo_eventer.finish(f"{TITLE} ECHO\n    - 键政大师！滚！")
            
    # 正则表达式检测
    for pattern in failedRegexs:
        if re.search(pattern, _msg):
            user.echoWarningd()
            await echo_eventer.finish(f"{TITLE} ECHO\n    - 键政大师！滚！")

    # 英文检测
    for word in failedEngWordsList:
        if word in _msg:
            user.echoWarningd()
            await echo_eventer.finish(f"{TITLE} ECHO\n    - 键政大师！滚！")

    if _msg == "棍母" or _msg == "棍母" or _msg == "██":
        await echo_eventer.finish("  ")
    # 如果用户未被封禁且提供了文本，则原样返回
    await echo_eventer.finish(_msg)
    
"""
捡垃圾功能

@author: Latingtude
"""

wasteTaker_event = on_command("cleanwaste", aliases={"捡垃圾"}, priority=5)

@wasteTaker_event.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    # 统一的随机概率列表
    # 映射关系更清晰，避免使用 index()
    # 属性： (名称, 金额)
    waste_options = [
        ("普通", 1), ("普通", 1), ("普通", 1), ("普通", 1),
        ("垃圾", 0), ("垃圾", 0), ("垃圾", 0), ("垃圾", 0),
        ("垃圾", 0), ("垃圾", 0), ("垃圾", 0), ("垃圾", 0),
        ("中级", 5), ("高级", 10), ("黄金", 100), ("钻石", 10000)
    ]
    
    # 从列表中随机选择一个
    waste_name, waste_money = random.choice(waste_options)
    
    msg = f"{TITLE} - 捡垃圾"
    
    user = User(str(event.get_user_id()))
    
    if user.isBanned():
        if user.playMode():
            msg += "\n    - 你他妈被封禁了还想捡垃圾？滚"
        else:
            msg += "\n    - 您的账号已被封禁，请联系管理员解封。"
        await wasteTaker_event.finish(msg)
    
    # 用户未被封禁，执行捡垃圾逻辑
    user.addScore(float(waste_money))
    user.save()
    
    msg += f"\n    - 你没钱了，你来捡垃圾。"
    msg += f"\n    - 垃圾属性："
    msg += f"\n          类型：{waste_name}"
    msg += f"\n          赚了：{waste_money}"
    msg += f"\n    - 你现在的积分是: {user.getScore():.2f}"
    
    await wasteTaker_event.finish(msg)
    
"""
排行榜功能

@author: Latingtude
"""

list_eventer = on_command("moneybest", aliases={"排行榜"}, priority=5)

@list_eventer.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} - 排行榜\n"
    
    # 确保文件夹存在，避免 os.listdir 报错
    data_path = "./userdata" # 注意: 这里应该使用 userInfoController.Data 中定义的路径
    if not os.path.exists(data_path):
        await list_eventer.finish(msg + "    - 暂无数据可供排名。")

    # 获取所有用户数据文件
    # 原始代码使用了 './database'，但 User 类中是 './userdata'，这里已更正
    user_files = os.listdir(data_path)
    
    user_scores = {}
    for filename in user_files:
        # 确保只处理有效的用户数据文件，这里假设文件名格式是 "QQ号.toolsbot_data"
        if filename.endswith(".toolsbot_data"):
            user_id = filename.split(".")[0]
            try:
                # 实例化用户对象并获取分数
                user = User(user_id)
                if not user.isBanned(): # 更好的做法是只展示未被封禁的用户
                    if user.name != "":
                        user_scores[user.name] = user.getScore()
                    else:
                        user_scores[user.id] = user.getScore()
            except Exception as e:
                # 捕获可能的读取错误，比如文件损坏
                print(f"Error reading user data for {user_id}: {e}")
                continue
    
    # 按分数降序排序，并保留前10名
    sorted_scores = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)[:10]

    # 检查是否有数据
    if not sorted_scores:
        await list_eventer.finish(msg + "    - 暂无数据可供排名。")
    
    # 格式化输出排行榜
    for rank, (user_name, score) in enumerate(sorted_scores, 1):
        msg += f"    - 第 {rank} 名：{user_name}，积分：{score:.2f}\n"

    await list_eventer.finish(msg)
    
"""
ban 函数
封禁用户

@author: Latingtude
"""

ban_function = on_command("ban", priority=10, permission=SUPERUSER)

@ban_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} 管理系统"
    ats = At(event.json())
    
    if len(ats) == 1:
        user = User(ats [0])
        user.banned = True
        user.save()
        msg += f"\n    - 已封禁用户 {user.id}。"
    elif len(ats) > 1:
        for userId in ats:
            user = User(userId)
            user.banned = True
            user.save()
            msg += f"\n    - 已封禁用户 {user.id}。"
        msg += f"\n    - 本次封禁 {len(ats)} 个用户。"
    else:
        msg += "\n    - 使用 ^ban [@用户] (可封禁多个)"
    
    await ban_function.finish(msg)
    
"""
Pardon 函数
解除用户封禁

@author: Latingtude
"""

pardon_function = on_command("pardon", priority=10, permission=SUPERUSER)

@pardon_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} 管理系统"
    ats = At(event.json())
    
    if len(ats) == 1:
        user = User(ats [0])
        user.banned = False
        user.save()
        msg += f"\n    - 已解封用户 {user.id}。"
    elif len(ats) > 1:
        for userId in ats:
            user = User(userId)
            user.banned = False
            user.save()
            msg += f"\n    - 已解封用户 {user.id}。"
        msg += f"\n    - 本次封禁 {len(ats)} 个用户。"
    else:
        msg += "\n    - 使用 ^pardon [@用户] (可封禁多个)"
        
    await pardon_function.finish(msg)
    
"""
BanList 函数
查看封禁用户列表

@author: Latingtude
"""

banlist_function = on_command("banlist", priority=10) # 普通用户也可以看 banlist

@banlist_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} 管理系统"
    
    # users
    users = os.listdir("./userdata")
    
    for _user in users:
        _user = _user.replace(".toolsbot_data", "")
        user = User(_user)
        
        if user.isBanned():
            msg += f"\n    - {user.id} 已被封禁"
            
    if msg == f"{TITLE} 管理系统":
        msg += "\n    - 当前没有被封禁的用户"
        
    await banlist_function.finish(msg)
    
"""
AccountStatus 函数
查看当前账号 / 其他账号是否被封禁

@author: Latingtude
"""

accountstatus_function = on_command("accountstatus", aliases={"accountStatus"}, priority=10)

@accountstatus_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} 当前账号情况"
    at = At(event.json())
    
    if len(at) == 0:
        
        user = User(event.get_user_id())
        
        ban = "解禁"
        if user.isBanned():
            ban = "封禁"
        
        msg += f"\n    - 当前您账号的情况："
        msg += f"\n        - 封禁状态：{ban}"
    else:
        
        user = User(at [0])
        
        ban = "解禁"
        if user.isBanned():
            ban = "封禁"
        
        msg += f"\n    - 当前该账号的情况："
        msg += f"\n        - 封禁状态：{ban}"
        
    await accountstatus_function.finish(msg)
    
"""
红包函数
给群友发红包

@author: Latingtude
"""

redpacket_function = on_command("redpacket", aliases={"发红包"}, priority=5)

@redpacket_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} - 发红包"
    user = User(event.get_user_id())
    
    if user.isBanned():
        if user.playMode():
            msg += "\n    - 你他妈被封禁了还想发红包？滚"
        else:
            msg += "\n    - 您的账号已被封禁，请联系管理员解封。"
        await redpacket_function.finish(msg)
    
    _msg = args.extract_plain_text().split(" ")
    
    if len(_msg) < 2:
        msg += "\n    - 使用 ^redpacket [金额] [数量] 来发红包"
        await redpacket_function.finish(msg)
    
    try:
        money = float(_msg [0])
        number = int(_msg [1])
    except ValueError:
        if user.playMode():
            msg += "\n    - 你他妈语法都不会还想发红包？滚"
        else:
            msg += "\n    - 语法错误或金额不是正整数"
        await redpacket_function.finish(msg)
        
    if money <= 0 or number <= 0:
        if user.playMode():
            msg += "\n    - 你他妈语法都不会还想发红包？滚"
        else:
            msg += "\n    - 语法错误或金额不是正整数"
        await redpacket_function.finish(msg)
        
    if user.getScore() < money:
        if user.playMode():
            msg += "\n    - 你他妈穷成这样还想发红包？滚"
        else:
            msg += "\n    - 余额不足"
        await redpacket_function.finish(msg)
        
    if number > 100:
        if user.playMode():
            msg += "\n    - 发红包数量过多。你他妈有钱不如做慈善。"
        else:
            msg += "\n    - 发红包数量过大。"
        await redpacket_function.finish(msg)
        
    # ok, start
    user.subtScore(money)
    user.save()
    
    perMoney = money / number
    
    msg += f"\n    - 成功发出 {number} 个红包，每个 {perMoney:.2f} 积分。请让群友使用 ^openredpacket 来领取。"
    
    # save
    redpacket = {
        "UserID": user.id,
        "Money": perMoney,
        "Number": number,
        "TakedUser": []
    }
    
    # open redpacket data
    redpacket_data_path = "./data/redpackets.json"
    
    if os.path.exists(redpacket_data_path):
        try:
            with open(redpacket_data_path, "r", encoding="utf-8") as f:
                redpackets = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {redpacket_data_path} is corrupted. Starting with an empty redpacket list.")
            redpackets = []
    else:
        redpackets = []
        
    redpackets.append(redpacket)
    with open(redpacket_data_path, "w", encoding="utf-8") as f:
        json.dump(redpackets, f, ensure_ascii=False, indent=4)
        
    await redpacket_function.finish(msg)
    
"""
openredpacket 函数
抢红包

@author: Copilot and Latingtude
"""

openredpacket_function = on_command("openredpacket", aliases={"抢红包"}, priority=5)

@openredpacket_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = f"{TITLE} - 抢红包"
    user = User(event.get_user_id())
    
    if user.isBanned():
        if user.playMode():
            msg += "\n   - 你他妈被封禁了还想抢红包？滚"
        else:
            msg += "\n   - 您的账号已被封禁，请联系管理员解封。"
        await openredpacket_function.finish(msg)
    
    # open redpacket data
    redpacket_data_path = "./data/redpackets.json"
    
    if os.path.exists(redpacket_data_path):
        try:
            with open(redpacket_data_path, "r", encoding="utf-8") as f:
                redpackets = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {redpacket_data_path} is corrupted. Starting with an empty redpacket list.")
            redpackets = []
    else:
        redpackets = []
        
    if len(redpackets) == 0:
        msg += "\n   - 当前没有可抢的红包。"
        await openredpacket_function.finish(msg)
    
    # 随机选择一个红包
    selected_index = random.randint(0, len(redpackets) - 1)
    selected_redpacket = redpackets[selected_index]
    
    if user.id in selected_redpacket["TakedUser"]:
        if user.playMode():
            msg += "\n   - 你他妈已经抢过这个红包了，再抢就变成██。"
        else:
            msg += "\n   - 您已经抢过这个红包了，不能重复抢。"
        await openredpacket_function.finish(msg)
    
    # 给用户加钱
    user.addScore(float(selected_redpacket["Money"]))
    user.save()
    
    msg += f"\n   - 抢到一个 {selected_redpacket['Money']:.2f} 积分的红包！"
    msg += f"\n   - 目前您的积分为 {user.getScore():.2f}。"
    
    # 更新红包数据
    selected_redpacket["Number"] -= 1
    selected_redpacket["TakedUser"].append(user.id)
    if selected_redpacket["Number"] <= 0:
        # 如果红包数量为0，移除该红包
        del redpackets[selected_index]
    else:
        # 否则更新红包信息
        redpackets[selected_index] = selected_redpacket    
    
        
    # 写入
    open("./data/redpackets.json", "w", encoding="utf-8").write(json.dumps(redpackets, ensure_ascii=False, indent=4))
    
    await openredpacket_function.finish(msg)
    
# esu 功能
fuck_eventer = on_command("fuck")

@fuck_eventer.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    # use api
    try:
        await bot.call_api("send_private_msg", user_id=event.user_id, message="You ****ed " + args.extract_plain_text())
    except ActionFailed:
        await fuck_eventer.finish("彩蛋无法触发。若该群禁止了私聊请先加 Bot 好友。")
    else:
        await fuck_eventer.finish("彩蛋触发。请查看私聊。")
        
"""
modifyname 函数

修改用户昵称
@author: Latingtude
"""

modifyname_function = on_command("modifyname", aliases={""}, priority=10)

@modifyname_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE + " Modify Name"
    user = User(event.get_user_id())
    _msg = args.extract_plain_text()
    
    user.name = _msg
    
    msg += "\n    - 名称修改完毕。你现在的新名称为：" + user.name + "。"
    
    
    user.save()
    await modifyname_function.finish(msg)

"""
bag 函数

查看目前包里都有啥
@author: Latingtude
"""

bag_function = on_command("bag", aliases={""}, priority=10)

@bag_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    msg = TITLE = " "
    user = User(event.get_user_id())
    _msg = args.extract_plain_text()
    
    # direct show items
    msg += f"\nRE: Toolsbot 背包"
    msg += f"\n    - 目前你包里有："
    items = user.boughtItems
    if len(items) == 0:
        msg += "\n    - 你包里是空的。"
    else:
        # precontrol
        lastitem = ""
        count = {}
        for item in items:
            if item == lastitem:
                items.remove(item)
                count[item] += 1
            lastitem = item
            
        for item in items:
            if item in count.keys():
                msg += f"\n    - {item} x{count[item]+1}"
            else:
                msg += f"\n    - {item}"
    
    await bag_function.finish(msg)