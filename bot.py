import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter  # 避免重复命名
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

# 初始化 NoneBot
nonebot.init(superusers={"2733392694"},command_start={"^"})

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)
driver.register_adapter(OnebotV11Adapter)

# 在这里加载插件
nonebot.load_plugins("./toolsbot/plugins")

if __name__ == "__main__":
    nonebot.run()