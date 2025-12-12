"""
mapInterpreter
"""

from typing import Literal

from toolsbot.configs import DATA_PATH, PLUG_PATH

from . import mapInterpreterLib as lib


def run(data: str):
    # data is a file under data/map/areas/.

    # add manage.py before file
    with open(DATA_PATH / "map" / "areas" / data, "r", encoding="utf-8") as f:
        file = f.read()
    with open(PLUG_PATH / "gamingController" / "mapInterpreterLib.py", "r", encoding="utf-8") as f:
        manageFile = f.read() + "\n\n"

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