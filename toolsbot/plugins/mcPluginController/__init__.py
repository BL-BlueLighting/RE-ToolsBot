
from nonebot import *
from nonebot.adapters.onebot.v11 import Message, Bot, MessageEvent
from nonebot.params import CommandArg
from mcstatus import JavaServer
import re

# 去除颜色代码
def strip_minecraft_colors(text: str) -> str:
    return re.sub(r"§[0-9A-FK-ORa-fk-or]", "", text)

mc_status = on_command("mcstatus", aliases={"mc服务器"}, priority=5)


@mc_status.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    # 解析命令参数，例如 ^mcstatus play.example.com:25565
    target = args.extract_plain_text().strip()
    if not target:
        await mc_status.finish("RE: ToolsBot Minecraft Plugin\n    - 用法：^mcstatus <地址>[:端口]")

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
        await mc_status.finish(f"查询失败：{type(e).__name__} - {e}")
        
    await mc_status.finish(msg)