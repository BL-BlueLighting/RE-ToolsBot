"""
Control finalescope_data \\ fs_data more file interpret.
"""
import toolsbot.plugins.userInfoController as dc
import configparser

class Door:
    def __init__(self, name: str, unlockCondition: list[str], reward: int):
        self.name = name
        self.unlockCondition = unlockCondition
        self.reward = reward
    
    def condition(self, user: dc.User) -> bool:
        """
        Check if the user meets the unlock conditions.
        """
        
        # check must condition
        global _condition_pass
        _condition_pass = False
        for condition in self.unlockCondition:
            if "finish" in condition:
                condition = condition.replace("finish ", "")
                open("./userdata/finaleScope/" + user.id + ".finalescope_data", "r", encoding="utf-8").read() # this is a ini
                config = configparser.ConfigParser()
                config.read("./userdata/finaleScope/" + user.id + ".finalescope_data",
                            encoding="utf-8")
                
                if config.get("Scope", "DoorsUnlock") != "":
                    if not condition in config.get("Scope", "DoorsUnlock").split(", "):
                        _condition_pass = False
                        return _condition_pass
                else:
                    _condition_pass = False
                    return _condition_pass
            
            elif "haveItem" in condition:
                condition = condition.replace("haveItem ", "")
                if not condition in user.boughtItems:
                    _condition_pass = False
                    return _condition_pass

            elif "autoUnlock" in condition:
                _condition_pass = True
                break
            
        return True
    
    
class FinaleScope:
    def __init__(self):
        self.doors = []
        
    def newDoor(self, name: str, unlockCondition: list[str], reward: int):
        self.doors.append(Door(name, unlockCondition, reward))