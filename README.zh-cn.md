<div align="center">
    <img src="./README.Logo.jpg" style="width: 128px;">
</div>


<h1 align="center">RE: ToolsBot</h1>

<p align="center">
    <a href="#">
        <img src="https://img.shields.io/badge/Version-1.4.0-blue">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/OneBot-v11-blue">
    </a>
</p>

<div align="center">
    <a href="./README.zh-cn.md">中文</a> | <a href="./README.md">English</a>
</div>

<p align="center"><i>优秀的 QQ Bot 实例</i></p>

> [!Warning]
>
> ToolsBot 已更新，请在 git pull 下来后，执行 python ./quickmove.py 来迁移用户数据

## 如何使用
先 git clone 下来整个项目。

`
git clone https://github.com/Latingtude/RE-ToolsBot.git
`

然后，使用下面这行命令安装所有依赖。

`
python ./install/installTB.py
`

或者，直接通过 pip 安装：

`
pip install -r ./install/requirements.txt
`

(只创建一个空项目，选择全局安装)

在所有的事情干完后，修改 `.env.dev` `.env.prod` `bot.py` 中的 SUPERUSER 为你自己的 QQ号码。

接下来，打开 `data/configuration_template.json`，修改其中的 AI_ApiKEY 项目为你的硅基流动 API Key。随后重命名为 `configuration.json`。
若不需要，请直接重命名为 `configuration.json`。

随后，运行 `nb run --reload` 来启动 bot.

## 这个 bot 怎么链接到 QQ？

去看 https://github.com/NapNeko/NapCatQQ.

## 感谢
> [!Note]
>
> 感谢以下项目，我参考了以下项目的部分代码。

<a href="https://github.com/yzyyz1387/nonebot_plugin_admin/">NoneBot Plugin Admin</a>

## 警告

> [!Warning]
>
> 该项目目前并不稳定。请不要直接克隆该项目，我没办法做到自检查代码的每一处角落。
>
> 如果你发现了任何问题，请在 `Github Issues` 中发表一个 Issue。