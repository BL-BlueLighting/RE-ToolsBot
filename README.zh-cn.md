<center><h1>RE: ToolsBot</h1></center>

![Version](https://img.shields.io/badge/Version-1.0.0-blue) ![Onebot Version](https://img.shields.io/badge/OneBot-v11-blue)

<center><a href="./README.zh-cn.md">中文</a> | <a href="./README.md">English</a></center>

## 这是什么玩意？
一个 QQ 的机器人。娱乐用。

## 咋用？
先 git clone 下来整个项目。

`
git clone https://github.com/Latingtude/RE-ToolsBot.git
`

然后，使用下面这行命令安装所有依赖。

`
nb create
`

(只创建一个空项目，选择全局安装)

在所有的事情干完后，修改 `.env.dev` `.env.prod` `bot.py` 中的 SUPERUSER 为你自己的 QQ号码。

接下来，打开 `data/configuration_template.json`，修改其中的 AI_ApiKEY 项目为你的硅基流动 API Key。随后重命名为 `configuration.json`。
若不需要，请直接重命名为 `configuration.json`。

随后，运行 `nb run --reload` 来启动 bot.

## 这个 bot 怎么链接到 QQ？

去看 https://github.com/NapNeko/NapCatQQ.
