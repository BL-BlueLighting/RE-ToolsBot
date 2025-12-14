
import json
import os
import random
import sqlite3
from typing import Any, Dict

import old_file.userInfoClasses as dc

print("RE: ToolsBot - Userdata 迁移工具")
print("迁移所有 userdata 下 .userdata 文件到 sqlite3 userdata.db")
print("")

_info = print
_erro = print

class Data:
    def __init__(self, id: str):
        """
        Data Class.

        Args:
            id (str): Platform ID.
        """
        self.id = id
        self.db_path = "./userdata.db"
        self._init_db()

    def _init_db(self):
        """初始化数据库和表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    ID TEXT PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Score INTEGER DEFAULT 0,
                    boughtItems TEXT DEFAULT '[]',
                    Ban TEXT DEFAULT '[]',
                    Warningd TEXT DEFAULT '[]',
                    DynamicExts TEXT DEFAULT '{}'
                )
            """)
            conn.commit()

    def check(self) -> bool:
        """
        Check userdata exists.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE ID = ?", (self.id,))
            return cursor.fetchone() is not None

    def writeData(self, userClass):
        """
        Write user data.
        Note: Because userClass is a user class, but user is defined after Data class.
        So I will not add type tip to it.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users
                (ID, Name, Score, boughtItems, Ban, Warningd, DynamicExts)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                userClass.id,
                userClass.name,
                userClass.score,
                json.dumps(userClass.boughtItems),
                json.dumps(userClass.banned),
                json.dumps(userClass.warningd),
                json.dumps(getattr(userClass, 'dynamicExts', {}))
            ))
            conn.commit()

    def readData(self) -> Dict[str, Any]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT ID, Name, Score, boughtItems, Ban, Warningd, DynamicExts
                    FROM users WHERE ID = ?
                """, (self.id,))
                row = cursor.fetchone()

                if row is None:
                    return {}

                return {
                    "ID": row[0],
                    "Name": row[1],
                    "Score": row[2],
                    "boughtItems": json.loads(row[3]),
                    "Ban": row[4] == "true",
                    "Warningd": int(row[5]),
                    "DynamicExts": json.loads(row[6])
                }
        except Exception as ex:
            _erro("Error: Failed to read data.\nInformation: \n" + str(ex))
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
        with open("./data/item.json", "r", encoding="utf-8") as f:
            itemJson: list[dict] = json.load(f)

        itemEffect = ""
        # fetch
        for _item in itemJson:
            if _item.get("Name", "") == item:
                itemEffect = _item.get("Effect")
                break

        if item == "iai" or item == "棍母" or item == "滚木" or item == "BL.BlueLighting":
            itemEffect = ["spe " + item]

        # _info(f"物品：{item} 的效果：" + itemEffect [0]) #type: ignore

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

        if "sign" in itemEffect[0]:  # type: ignore
            _info(f"SIGN MODE")
            # get *x

            _x = itemEffect[0].split(" ")[1]  # type: ignore

            # out x
            _x = _x.replace("x", "")

            # read boost
            with open("./data/boostMorningd.json", "r", encoding="utf-8") as f:
                boosts = json.load(f)

            # append boost
            boosts.append({self.id: int(_x)})

            # write boost
            with open("./data/boostMorningd.json", "w", encoding="utf-8") as f:
                json.dump(boosts, f)

            self.boughtItems.remove(item)
            return f"{_x}x 倍票已使用。下次签到将会获得更多积分。"

        elif "ticket" in itemEffect[0]:  # type: ignore
            _info(f"TICKET MODE")
            _randomNum = random.randint(1, 1000000000000)  # 人：傻逼
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

        elif "playmode" in itemEffect[0]:  # type: ignore
            if "enable" in itemEffect[0]:  # type: ignore
                self.boughtItems.remove(item)
                self.boughtItems.append("play")
                self.save()
                return "已启用娱乐模式。"
            else:
                if "play" in self.boughtItems:
                    self.boughtItems.remove("play")
                    self.save()
                return "已关闭娱乐模式。"
        elif "spe" in itemEffect[0]:  # type: ignore
            if "iai" in itemEffect[0]:  # type: ignore
                return "芝士 ARG 作者"
            elif "棍母" or "滚木" in itemEffect[0]:  # type: ignore
                return "？请不要使用空白物品谢谢"
            elif "BL.BlueLighting" in itemEffect[0]:  # type: ignore
                return "芝士 Bot 主"
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
        return self.banned  # type: ignore

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

# begin
enter = input("开始迁移？(y/N) ")
if enter.lower() != "y":
    print("迁移停止。")
    exit()

# get all userdata files
_userdatas = os.listdir("./userdata")

for _userdata in _userdatas:
    if _userdata.endswith(".toolsbot_data"):
        oldUsr = dc.User(_userdata.replace(".toolsbot_data", ""))
        newUsr = User(oldUsr.id)

        # move
        newUsr.score = oldUsr.score
        newUsr.boughtItems = oldUsr.boughtItems
        newUsr.name = oldUsr.name
        newUsr.banned = oldUsr.banned

        newUsr.save()
        print(f"迁移用户 '{oldUsr.id}' 的数据成功。")

print("迁移完毕。")