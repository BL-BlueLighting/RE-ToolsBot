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
import userInfoClasses as uic

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

argGodMakerController
"""

TITLE = "RE: ToolsBot"
TIMEDATESTR = "%Y-%d-%m-%H-%M-%S"

class GMUser:
    def __init__(self, userEntity: uic.User, status: str = "凉菜起"):
        self.user = userEntity
        self.status = status
        self.rating = 0
        self.level = 1
        self.pausing = False
        self.beginPause: datetime.datetime = None
        self.load()
    
    def load(self):
        if not os.path.exists("./data/godmaker/" + self.user.id + ".gmdata"):
            self.initData() # 没有存档，初始化
            return
        
        data = json.load(open(f"./data/godmaker/{self.user.id}.gmdata", "r", encoding="utf-8"))
        
        self.status = data ["Status"]
        self.rating = int(data ["Rating"])
        self.level = int(data ["Level"])
        self.pausing = bool(data ["Pausing"])
        self.beginPause = datetime.datetime.strptime(data.get("BeginPause", "2025-01-01-01-01-01"), TIMEDATESTR)
        return
    
    def initData(self):
        data = {
            "ID": self.user.id,
            "Status": self.status,
            "Rating": self.rating,
            "Level": self.level,
            "Pausing": False,
            "BeginPause": "2025-01-11-01-01-01"
        }
        
        open("./data/godmaker/"+self.user.id+".gmdata", "w", encoding="utf-8").write(json.dumps(data))
        return
    
    def save(self):
        data = {
            "ID": self.user.id,
            "Status": self.status,
            "Rating": self.rating,
            "Level": self.level,
            "Pausing": self.pausing,
            "BeginPause": datetime.datetime.now().strftime(TIMEDATESTR)
        }
        
        open("./data/godmaker/"+self.user.id+".gmdata", "w", encoding="utf-8").write(json.dumps(data))
        return
    
    def uplevel(self):
        if random.randint(1, 10) < 5:
            self.level += 1
            self.save()
            return True
        return False
    
    def setStatus(self, status: str):
        self.status = status
        self.save()
        
    def getStatus(self) -> str:
        self.save()
        return self.status + f" {self.level} 层"
    
    def getRating(self) -> int:
        self.save()
        return self.rating
    
    def upRating(self, rating: int):
        self.rating += rating
        self.save()
        return
    
    def downRating(self, rating: int):
        self.rating -= rating
        self.save()
        return
    
    def pause(self):
        self.pausing = True
        self.save()
        return
    
    def checkPause(self):
        if (datetime.datetime.now() - self.beginPause).seconds > 60:
            self.pausing = False
            return True
        return False
        
STATUSES = [
    "凉菜起",
    "杨倒带",
    "梁才起",
    "T3",
    "群u",
    "212",
    "derakkuma",
    "鳝丝",
    "国人",
    "小一",
    "Hello World",
    "是你让我扁",
    "是你让我神经w",
    "何异味。",
    "T1",
    "T2",
    "T0",
    "Richard",
    "Copilot",
    "DeepSeek",
    "Gemini",
    "文档",
    "退群。",
    "cutebox",
    "小绿叶",
    "SCP-Cloud-373",
    "他妈手抄",
    "令人忍俊不禁",
    "你们在瞎搞",
    "我们在瞎搞",
    "瞎搞军团",
    "诗人v1",
    "诗人v2",
    "门口午睡",
    "iai 更新日期",
    "烦人的英语",
    "德粒沙壁",
    "一群傻逼活该被炸服",
    "这么强",
    "那么扁",
    "邮差是吾辈",
    "你真的是邮差吗",
    "www.114514@qq.com",
    "职业中",
    "失业中",
    "点不动，，，",
    "Original",
    "Plus",
    "GReeN",
    "GReeN Plus",
    "ORANGE",
    "ORANGE Plus",
    "PiNK",
    "PiNK Plus",
    "murasaki",
    "murasaki Plus",
    "MiLK",
    "MiLK Plus",
    "FiNALE",
    "DX Original",
    "DX Plus",
    "DX Splash",
    "DX Splash Plus",
    "DX UNiVERSE",
    "DX UNiVERSE Plus",
    "DX FESTiVAL",
    "DX FESTiVAL Plus",
    "DX BUDDiES",
    "DX BUDDiES Plus",
    "DX PRiSM",
    "DX PRiSM Plus",
    "DX Circle",
    "PΛNDΘRΛ BΘXXX",
    "PANDORA PARADOXX"
    "KALEID<>SCOPE",
    "Xaleid<>scopiX",
    "Virtual to Live",
    "QZKago Requiem",
    "FFT",
    "Alea jacta est!",
    "系ぎて",
    "King of Performai",
    "WEC",
    "Abstract",
    "Undertale",
    "Underverse",
    "SP!DUSTTALE",
    "DUSTTALE",
    "雨刮器",
    "After Pandora",
    "NightTheater",
    "Deltarune Chapter"
]

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
lcgodmaker 函数

让我们修 ARG 仙。
@author: Latingtude
"""

lcgodmaker_function = on_command("lcgodmaker", priority=10)

@lcgodmaker_function.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    user = uic.User(event.get_user_id())
    gmUser = GMUser(user)
    _msg = args.extract_plain_text()
    
    # 我可以说这个工作量真的很大
    cargs = _msg.split(" ")
    act = cargs [0]
    
    _fc = lcgodmaker_function
    fns = _fc.finish
    
    if act == "list" or act == "":
        await fns(f"""RE: ToolsBot - ARG 修仙系统
    欢迎来到 ARG 修仙系统！
    本命令支持的操作如下：
        - list: 显示操作列表
        - begin: 开始修仙。
        - info: 显示修仙信息，如段位。
        - pk: 和他人 pk。
        - best: 排行榜。
        - break: 结束修仙。
    目前 ARG 修仙系统共有 {len(STATUSES)} 个段位。""")
        
    elif act == "begin":
        if gmUser.pausing == False:
            gmUser.pause()
            await fns(f"""RE: ToolsBot - ARG 修仙系统
        - 您当前段位：{gmUser.getStatus()};
        - 正在尝试晋升：{gmUser.status} {gmUser.level + 1} 层
        - 请等待一分钟后再来 break，或者 break 掉来继续操作。""")
        else:
            await fns(f"""RE: ToolsBot - ARG 修仙系统
        - 您正在试图晋升，请不要再次使用。
        - 距离 break 时间：{str((datetime.datetime.now() - gmUser.beginPause).seconds - 60).replace("-", "")}""")
        
    elif act == "info":
        await fns(f"""RE: ToolsBot - ARG 修仙系统
    - 用户 ID：{gmUser.user.id}
    - 用户段位：{gmUser.getStatus()}
    - RATING：{gmUser.rating}""")
    
    elif act == "break":
        
        if len(cargs) == 2:
            gmUser.pausing = False
            gmUser.save()
            await fns(f"""RE: ToolsBot - ARG 修仙系统
    - 已强制结束修仙。""")           
        else:
            if gmUser.checkPause():
                rmsg = "RE: ToolsBot - ARG 修仙系统\n"
                
                # checking level, 5 to up status.
                if gmUser.level < 5:
                    gmUser.level += 1
                    gmUser.rating += random.randint(1000, 9999)
                    gmUser.save()
                    rmsg += "    - 您的等级已晋升。\n    - 目前等级：" + gmUser.getStatus()
                else:
                    gmUser.level = 1
                    if STATUSES.index(gmUser.status) == len(STATUSES) - 1:
                        rmsg += "    == PERFECT CHALLENGE ==\n    - 目前没有更新的段位。请等待 PERFECT CHALLENGE 第一赛季登场。"
                    else:
                        gmUser.rating += random.randint(1000, 9999)
                        gmUser.setStatus(STATUSES [STATUSES.index(gmUser.status) + 1])
                        rmsg += "    - 您的等级已晋升。\n    - 目前等级：" + gmUser.getStatus()
                    gmUser.save()
                
                await fns(rmsg)
            else:
                await fns("""RE: ToolsBot - ARG 修仙系统\n    - 请使用 ^lcgodmaker break sure 来强制结束修仙。""")
    
    elif act == "pk":
        rmsg = "RE: ToolsBot - ARG 修仙 - Global PK"
        gmConfig = json.load(open("./data/gmConfig.json", "r", encoding="utf-8"))
        
        rmsg += "\n    - 当前赛季：" + gmConfig.get("Status", "???") + ""
        rmsg += "\n    - 您的 Rating：" + str(gmUser.rating) + ""
        rmsg += "\n    - G L O B A L . P . K . - 开场"
        
        if len(cargs) == 1:
            cargs.append("") #给代码擦屁股
        
        if cargs [1] == "with":
            qq = At(event.json()) [0]
            
            if qq == "all":
                rmsg += "\n    - 我的妈呀，你对战全体成员？"
                await fns(rmsg)
            
            if gmConfig.get("PKEnabled") == False:
                rmsg += "\n    - P.K. 暂时未揭幕。"
                await fns(rmsg)
                
            _pking = json.load(open("./data/gmPKing.json", "r", encoding="utf-8"))
            pking = {}
            pkusers = []
            
            for pk in _pking:
                pking.update({pk.split(":") [0]:pk.split(":") [1]})
                pkusers.append(pk.split(":") [0])
                pkusers.append(pk.split(":") [1])
            
            if gmUser.user.id in pkusers:
                rmsg += "\n    - 你已经在 P.K. 中了。\n    - 使用 ^lcgodmaker pk status 来查看 P.K. 进度。"
                await fns(rmsg)          
            
            pkinfo = {
                "Users": [gmUser.user.id, qq],
                "StartTime": datetime.datetime.now().strftime(TIMEDATESTR),
                "Redeem": random.randint(1000, 9999)
            }
            
            _pki = json.load(open("./data/gmPKinfo.json", "r"))
            _pki.append(pkinfo)
            json.dump(_pki, open("./data/gmPKinfo.json", "r+"))
            
            _pking.append(f"{gmUser.user.id}:{qq}")
            json.dump(_pking, open("./data/gmPKing", "r+"))
            
            rmsg += "\n    - 你与 " + qq + " 开始 P.K."
            rmsg += "\n    - 对方目前段位：" + GMUser(uic.User(qq)).getStatus()
            rmsg += "\n    - 您目前段位：" + gmUser.getStatus()
            rmsg += "\n    - 持续时间：60 分钟，请在结束前与对方高至少一等级来获胜！\n   - 获胜奖励：" + str(pkinfo.get("Redeem")) + " 积分。"
            
            await fns(rmsg)
        
        elif cargs [1] == "status":
            rmsg = "RE: ToolsBot - ARG 修仙 - P.K. 过程"
            _pking = json.load(open("./data/gmPKing.json", "r", encoding="utf-8"))
            pking = {}
            pkusers = []
            otherUserQQ = ""
            pkStr = ""
            
            for pk in _pking:
                pking.update({pk.split(":") [0]:pk.split(":") [1]})
                pkusers.append(pk.split(":") [0])
                pkusers.append(pk.split(":") [1])
                if gmUser.user.id in pk:
                    pkStr = pk
                    otherUserQQ = pk.replace(f"{gmUser.user.id}", "")
                    otherUserQQ = otherUserQQ.replace(":", "")

            if not user.id in pkusers:
                rmsg += "    - 没有参加 P.K，请参加一次 P.K 再来查看。"
                await fns(rmsg)
            
            # get statuses
            otherUser = GMUser(uic.User(otherUserQQ))
            
            rmsg += "\n您的段位：" + gmUser.getStatus()
            rmsg += "\n对方段位：" + otherUser.getStatus()
            
            # pk
            pkLevelBig = max(STATUSES.index(otherUser.status), STATUSES.index(gmUser.status))
            pkLevelMin = min(STATUSES.index(otherUser.status), STATUSES.index(gmUser.status))
            global bestBig, whoBest
            bestBig = 0
            whoBest = 0
            
            if pkLevelBig == pkLevelMin:
                rmsg += "\n您和对方的段位持平。"
                # 查询几级
                if otherUser.level == gmUser.level:
                    rmsg += "\n您和对方的层持平。"
                    await fns(rmsg)
                    
                pkNLevelBig = max(otherUser.level, gmUser.level)
                if pkNLevelBig == otherUser.level:
                    rmsg += "\n对方比您高 " + str(otherUser.level - gmUser.level) + " 个层。"
                    whoBest = 0
                else:
                    rmsg += "\n您比对方高 " + str(otherUser.level - gmUser.level) + " 个层。"
                    whoBest = 1
                
            else:
                if pkLevelBig == STATUSES.index(otherUser.status):
                    bestBig = 1
                
                if bestBig:
                    rmsg += "\n对方比您高 " + str(pkLevelBig - pkLevelMin) + " 个段位。"
                    whoBest = bestBig
                else:
                    rmsg += "\n您比对方高 " + str(pkLevelBig - pkLevelMin) + " 个段位。"
                    whoBest = bestBig
            
            # 检查是否超时
            
            _pki = json.load(open("./data/gmPKinfo.json", "r"))
            users = pkStr.split(":")
            pki = {}
            
            for __pki in _pki:
                if __pki.get("Users") == users:
                    pki = __pki
                    
            beginTime = datetime.datetime.strptime(pki.get("StartTime", ""), TIMEDATESTR)
            if (datetime.datetime.now() - beginTime).seconds == 60 * 60:
                rmsg += "\n    - 比赛时间到！"
                if whoBest:
                    rmsg += "\n    - " + gmUser.user.id + " 获胜！"
                    redeem = random.randint(1000,9999)
                    rmsg += "\n    - 获得 " + str(redeem) + " Rating & 积分!"
                    gmUser.upRating(redeem)
                    gmUser.save()
                    gmUser.user.score += redeem
                    gmUser.user.save()
                else:
                    rmsg += "\n    - " + otherUser.user.id + " 获胜！"
                    redeem = random.randint(1000,9999)
                    rmsg += "\n    - 获得 " + str(redeem) + " Rating & 积分!"
                    otherUser.upRating(redeem)
                    otherUser.save()
                    otherUser.user.score += redeem
                    otherUser.user.save()
                
                # 删除
                del _pki [_pki.index(pki)]
                json.dump(_pki, open("./data/gmPKinfo.json", "w"))

            await fns(rmsg)
        elif cargs [1] == "season":
            rmsg = "RE: ToolsBot - ARG 修仙 GLOBAL.P.K - 赛季信息"
            rmsg += "\n    - 当前赛季：" + gmConfig.get("Status", "???") + ""
            rmsg += "\n    - 您的 Rating：" + str(gmUser.rating) + ""
            rmsg += "\n    - G L O B A L . P . K . - 开场"
            rmsg += "\n    - 目前正在进行的 PK："
            _pking = json.load(open("./data/gmPKing.json", "r", encoding="utf-8"))
            
            for pk in _pking:
                rmsg += f"\n        - {pk.split(":") [0]} 对战 {pk.split(":") [1]}"
            
            if _pking == []:
                rmsg += f"\n        - 赛季未揭幕或没有一个人开始对战。"
            
        else:
            rmsg = """RE: ToolsBot - ARG 修仙 GLOBAL.P.K.
    - 使用 ^lcgodmaker pk with @[XXX] 来和一个人发起 PK.
    - 使用 ^lcgodmaker pk status 来查看和另一个人发起的 PK 的相关信息。
    - 使用 ^lcgodmaker pk season 来查看赛季信息。"""

        await fns(rmsg)
            
        
    elif act == "best":
        rmsg = "RE: ToolsBot - ARG 修仙排行榜\n"
        # 确保文件夹存在，避免 os.listdir 报错
        data_path = "./data/godmaker" # 注意: 这里应该使用 userInfoController.Data 中定义的路径
        if not os.path.exists(data_path):
            await fns(rmsg + "    - 暂无数据可供排名。")

        # 获取所有用户数据文件
        # 原始代码使用了 './database'，但 User 类中是 './userdata'，这里已更正
        user_files = os.listdir(data_path)
        
        user_scores = {}
        for filename in user_files:
            # 确保只处理有效的用户数据文件，这里假设文件名格式是 "QQ号.gmdata"
            if filename.endswith(".gmdata"):
                user_id = filename.split(".")[0]
                try:
                    # 实例化用户对象并获取分数
                    user = GMUser(uic.User(user_id))
                    user_scores[user.user.id] = user.rating
                except Exception as e:
                    # 捕获可能的读取错误，比如文件损坏
                    print(f"Error reading user data for {user_id}: {e}")
                    continue
        
        # 按分数降序排序，并保留前10名
        sorted_scores = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)[:10]

        # 检查是否有数据
        if not sorted_scores:
            await fns(rmsg + "    - 暂无数据可供排名。")
        
        # 格式化输出排行榜
        for rank, (user_name, score) in enumerate(sorted_scores, 1):
            rmsg += f"    - 第 {rank} 名：{user_name}，Rating：{score:.2f}\n"

        await fns(rmsg)
    
    else:
        await fns("RE: ToolsBot - ARG 修仙系统\n    - 未知指令。")