# 该模块建造了 MapContent 相关内容，作为解释器的主要加载 library.

#from toolsbot.plugins.gamingController import MapUser
#上面这行造成循环引用了，删了
import json
from typing import Literal


class MapContent:

    def __init__(self):
        self.area = self.Area
        self.act = self.Action
        self.red = self.Redeem

    class Action:
        def __init__(self, Action: str):
            self.act = Action

        def interpret(self):
            return self.act

    class Redeem:
        def __init__(self, ID: int, Name: str, Need: int, PerfectChallenge: bool = False, ReviewChallenge: bool = False, Challenge: list = [], FinishMessage: str = "", Actions: list = [], End: bool = True):
            self.id = ID
            self.name = Name
            self.need = Need
            self.actions = Actions
            self.perfectChallenge = PerfectChallenge
            self.reviewChallenge = ReviewChallenge
            self.end = End
            self.challenge = Challenge
            self.finishMessage = FinishMessage

        def interpret(self):
            return self.id, self.name, self.need, self.actions, self.perfectChallenge, self.reviewChallenge, self.end, self.challenge, self.finishMessage

        def __call__(self) -> tuple:
            """ INTERPRET THE ACTION """
            for action in self.actions:
                actC = action.interpret()
                if "points" in actC:
                    if "add" in actC:
                        return "addpoints", actC.split(" ") [2]
                    elif "del" in actC:
                        return "delpoints", actC.split(" ") [2]
                    elif "set" in actC:
                        return "setpoints", actC.split(" ") [2]

                elif "lcgodmaker" in actC:
                    if "levelup" in actC:
                        return "perfectChallenge", f"ARG 修仙等级提高 {actC.split(" ") [2]} 级别后，@Bot主 来解除 PERFECT CHALLENGE 锁。"

                elif "send" in actC:
                    if "content" in actC:
                        return "reviewChallenge", actC.split(" ") [2]

            for action in self.challenge:
                actC = action.interpret()

                if "lcgodmaker" in actC:
                    if "levelup" in actC:
                        return "perfectChallenge", f"ARG 修仙等级提高 {actC.split(" ") [2]} 级别后，@Bot主 来解除 PERFECT CHALLENGE 锁。"

                elif "send" in actC:
                    if "content" in actC:
                        return "reviewChallenge", actC.split(" ") [2]

            return ()

    class Area:
        def __init__(self, MapName: str, MapID: int, Redeems: list, Start: int, AllKMS: int, Finish: int = 0, End: int = 0):
            self.mapName = MapName
            self.mapID = MapID
            self.redeems = Redeems
            self.start = Start
            self.end = End
            self.allKMS = AllKMS
            self.finish = Finish

        def interpret(self):
            return self.mapName, self.mapID, self.redeems, self.start, self.end, self.allKMS, self.finish

class MainInterpret:
    def __init__(self, mapEntity: MapContent.Area):
        self.mapName = mapEntity.mapName
        self.mapID = mapEntity.mapID
        self.redeems: list[MapContent.Redeem] = mapEntity.redeems
        self.start = mapEntity.start
        self.end = mapEntity.end
        self.allKMS = mapEntity.allKMS

    def interpret(self, userObject, action: Literal["select", "addkm", "checkredeem", "redeem", "isend", "nextRedeem"], params: list = []):
        # userObject: uic.User
        user_id = userObject.super.id

        # read data
        with open('./data/map/' + user_id + ".gmData", "r", encoding="utf-8") as f:
            mapData = json.load(f)

        if action == "select":
            mapData ["MapSelect"] = self.mapName
            mapData ["MapKilometres"] = 0 # 已走路程
            mapData ["MapNextRedeem"] = self.redeems [0].need
            mapData ["MapRecentKMetres"] = 0 # 之前走的总和路程
            mapData ["MapRecentRedeems"] = []
            # dump
            with open('./data/map/' + user_id + ".gmData", "w", encoding="utf-8") as f:
                json.dump(mapData, f, ensure_ascii=False, indent=4)

        elif action == "addkm":
            mapData ["MapKilometres"] += params [0]
            mapData ["MapRecentKMetres"] += params [0]
            mapData ["MapNextRedeem"] -= params [0]
            # dump
            with open('./data/map/' + user_id + ".gmData", "w", encoding="utf-8") as f:
                json.dump(mapData, f, ensure_ascii=False, indent=4)

        elif action == "checkredeem":
            if mapData ["MapKilometres"] >= self.redeems [len(mapData ["MapRecentRedeems"]) + 1].need:
                return True
            else:
                return False

        elif action == "redeem":
            # check requirement
            if mapData ["MapKilometres"] >= self.redeems [len(mapData ["MapRecentRedeems"]) + 1].need:
                mapData ["MapKilometres"] -= self.redeems [len(mapData ["MapRecentRedeems"]) + 1].need
            else:
                return

            act = self.redeems [len(mapData ["MapRecentRedeems"]) + 1] ()

            if act [0] == "addpoints":
                userObject.super.addScore(float(act [1]))

            elif act [0] == "delpoints":
                userObject.super.subtPoints(float(act [1]))

            elif act [0] == "setpoints":
                userObject.super.score = float(act [1])

            elif act [0] == "perfectChallenge":
                lockInfo = [True, {
                    "Why": "PERFECT CHALLENGE",
                    "HowUnlock": act [1]
                }]
                mapData ["Locking"] = lockInfo

            elif act [0] == "reviewChallenge":
                lockInfo = [True, {
                    "Why": "REVIEW CHALLENGE",
                    "HowUnlock": act [1]
                }]
                mapData ["Locking"] = lockInfo

            elif act [0] == "addkm":
                userObject.addKMs(act [1])

            mapData ["MapRecentRedeems"].append(self.redeems [len(mapData ["MapRecentRedeems"]) + 1].id)
            mapData ["MapNextRedeem"] = self.redeems [len(mapData ["MapRecentRedeems"]) + 1].need
            # dump
            with open('./data/map/' + user_id + ".gmData", "w", encoding="utf-8") as f:
                json.dump(mapData, f, ensure_ascii=False, indent=4)

        elif action == "isend":
            if mapData ["MapKilometres"] >= self.end:
                return True
            else:
                return False

        elif action == "nextRedeem":
            mapData ["MapRecentRedeems"].append(self.redeems [len(mapData ["MapRecentRedeems"]) + 1].id)
            mapData ["MapNextRedeem"] = self.redeems [params [0] + 1].need
            # dump
            with open('./data/map/' + user_id + ".gmData", "w", encoding="utf-8") as f:
                json.dump(mapData, f, ensure_ascii=False, indent=4)
            # this is force next redeem, redeem is trigger by user, but nextRedeem is trigger by bot self.

        userObject.save()
        userObject.super.save()
        userObject.load()
# end
