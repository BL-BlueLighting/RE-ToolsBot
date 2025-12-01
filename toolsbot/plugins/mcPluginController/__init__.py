
import json
import re
from typing import Dict, List

from mcstatus import JavaServer
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.params import CommandArg


# 去除颜色代码
def strip_minecraft_colors(text: str) -> str:
    return re.sub(r"§[0-9A-FK-ORa-fk-or]", "", text)

mc_status = on_command("mcstatus", aliases={"mc服务器"}, priority=5)

@mc_status.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    # 解析命令参数，例如 ^mcstatus play.example.com:25565
    target = args.extract_plain_text().strip()
    if not target:
        await mc_status.finish("RE: ToolsBot Minecraft Plugin\n    - 用法：^mcstatus query <地址>[:端口]\n    - 用法：^mcstatus look [服务器名]\n    - 用法：^mcstatus add [名称] ipaddress=[IP]:[端口，不填默认 25565]")

    _args = args.extract_plain_text().split(" ")
    if _args [0] == "query":
        target = target.replace("query ", "") # 替换 query 参数为棍母
        # 分离地址和端口（默认 25565）
        if ":" in target:
            host, port = target.split(":", 1)
            port = int(port)
        else:
            host, port = target, 25565

        try:
            server = JavaServer(host, port)
            status = server.status()

            motd = strip_minecraft_colors(status.description)
            online = status.players.online
            maxp = status.players.max
            latency = round(status.latency, 1)

            msg = (
                f"RE: ToolsBot Minecraft Plugin\n"
                f"    - 🌍 服务器：{host}:{port}\n"
                f"    - 📋 MOTD：\n    {motd}\n"
                f"    - 👥 在线人数：{online}/{maxp}\n"
                f"    - 📡 延迟：{latency} ms"
            )
        except Exception as e:
            await mc_status.finish(f"RE: ToolsBot Minecraft Plugin\n    - 查询失败：{type(e).__name__} - {e}")

    elif _args [0] == "look":
        servers = json.loads(open("./data/mcServers.json", "r", encoding="utf-8").read())
        server = {}

        for _server in servers:
            print("Name:" + _server.get("Name")) # type: ignore
            print("Looking Name:" + " " +target.replace("look ", ""))
            if _server.get("Name") == target.replace("look ", ""):
                server = _server

        if server == {}:
            msg = (
                f"RE: ToolsBot Minecraft Plugin\n"
                f"    - 🌍 服务器：{target.replace('look ', '')} (Undefined)\n"
                f"    - 未找到该服务器的任何信息。"
            )
            await mc_status.finish(msg)

        host, port = server.get("Address", ["", 0])

        if host == "" and port == 0:
            msg = (
                f"RE: ToolsBot Minecraft Plugin\n"
                f"    - 🌍 服务器：{target.replace('look ', '')} ({host}, {port})\n"
                f"    - 很抱歉，配置错误导致该服务器无法被查询。"
            )
            await mc_status.finish(msg)

        try:
            server = JavaServer(host, port)
            status = server.status()

            motd = strip_minecraft_colors(status.description)
            online = status.players.online
            maxp = status.players.max
            latency = round(status.latency, 1)

            msg = (
                f"RE: ToolsBot Minecraft Plugin\n"
                f"    - 🌍 服务器：{target.replace('look ', '')} ({host}:{port})\n"
                f"    - 📋 MOTD：\n    {motd}\n"
                f"    - 👥 在线人数：{online}/{maxp}\n"
                f"    - 📡 延迟：{latency} ms"
            )
        except Exception as e:
            await mc_status.finish(f"RE: ToolsBot Minecraft Plugin\n    - 查询失败：{type(e).__name__} - {e}")

    elif _args [0] == "add":
        # split name and address
        _name, _address = target.split("ipaddress=")
        _name = _name.replace("add ", "")

        _l_address = _address.split(":")

        _ip = ""
        _port = 0

        if len(_l_address) == 1:
            _ip = _l_address [0]
            _port = 25565
        else:
            _ip = _l_address [0]
            _port = _l_address [1]

        # test
        print(_l_address)
        print(_ip, _port)

        try:
            server = JavaServer(_ip, int(_port))
            status = server.status()
        except TypeError:
            msg = (
                f"RE: ToolsBot Minecraft Plugin\n"
                f"    - 无法添加，原因：请输入正确的服务器端口"
            )
            await mc_status.finish(msg)
        except Exception as e:
            print(e.__str__())
            msg = (
                f"RE: ToolsBot Minecraft Plugin\n"
                f"    - 无法添加，原因：服务器无法联通或端口不正确\\封禁 Bot IP"
            )
            await mc_status.finish(msg)

        # make configuration file
        _config = {
            "Name": _name,
            "Address": [_ip, int(_port)]
        }

        # write in
        servers: list[dict] = json.loads(open("./data/mcServers.json", "r", encoding="utf-8").read())
        servers.append(_config)
        json.dump(servers, open("./data/mcServers.json", "w", encoding="utf-8"))

        # result send
        msg = (
            f"RE: ToolsBot Minecraft Plugin\n"
            f"    - 添加成功！使用 ^mcserver look {_name} 来查看该服务器。"
        )
    await mc_status.finish(msg)