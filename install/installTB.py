"""
RE: ToolsBot 全自动安装
"""

import os, platform

print("RE: ToolsBot 全自动安装向导")
print(":: 请稍等，正在检查系统环境")

_plat = "Win"

if platform.system() == "Linux":
    _plat = "Linux"
else:
    print(":: 很抱歉，您当前系统并不支持全自动安装。请手动安装。")
    exit()

run = os.system

print(":: 接下来 Bot 将会开始安装，请勿进行任何操作。")

"""
print(":: 正在安装 pipx...")
run("pip install pipx") # install pipx
print(":: pipx 安装完毕。\n")

print(":: 正在启动其他命令行安装 nonebot cli...")
run("start cmd /k pipx install nb-cli && exit") # install nonebot cli
print(":: nonebot cli 安装完毕。\n")

print(":: 正在启动其他命令行确认 Path...")
run("start cmd /k pipx ensurepath && exit") # ensurepath
print(":: 确认 Path 完毕。\n")

print(":: 正在安装 Bot 所需依赖...")
run("pip install -r ./requirements.txt") # install all requirements
print(":: Bot 所需依赖安装完毕。")
"""

if _plat == "Win":
    run("start cmd /k ./Win.bat")
else:
    run("bash ./Linux.sh")

print(":: Bot 安装完毕。")
print(":: 打开新的命令行，进入 Bot 目录，运行 nb run --reload 来启动 Bot.")