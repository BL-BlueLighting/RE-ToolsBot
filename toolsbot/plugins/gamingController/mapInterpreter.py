"""
mapInterpreter
"""

from typing import Literal

import toolsbot.plugins.gamingController.mapInterpreterLib as lib


def run(data: str):
    # data is a file under data/map/areas/.

    # add manage.py before file
    file = open("./data/map/areas/" + data, "r", encoding="utf-8").read()
    manageFile = open("./toolsbot/plugins/gamingController/mapInterpreterLib.py", "r", encoding="utf-8").read() + "\n\n"

    # remove contents before # BEGIN and after # EOF
    file = file.split("# BEGIN")[1].split("# EOF")[0]

    file = manageFile + file

    # exec
    namespace = {}
    exec(file, namespace)

    # return scope
    return namespace['area']

def interpret(area: lib.MapContent.Area, userObject, action: Literal["select", "addkm", "checkredeem", "redeem", "isend", "nextRedeem"], params: list = []):
    object_ = lib.MainInterpret(area)
    res = object_.interpret(userObject, action, params)
    condition = res is None or res != False
    return condition

def runAndInterpret(data: str, userObject, action, params):
    area = run(data)
    return interpret(area, userObject, action, params)