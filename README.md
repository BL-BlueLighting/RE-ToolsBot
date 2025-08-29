<div align="center">
    <img src="./README.Logo.jpg" style="width: 128px;">
</div>

<h1 align="center">RE: ToolsBot</h1>

<p align="center">
    <a href="#">
        <img src="https://img.shields.io/badge/Version-1.0.0-blue">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/OneBot-v11-blue">
    </a>
</p>

<div align="center">
    <a href="./README.zh-cn.md">中文</a> | <a href="./README.md">English</a>
</div>

<p align="center"><i>Perfect Bot for QQ.</i></p>

## How to use it?
First, clone this project.

`
git clone https://github.com/Latingtude/RE-ToolsBot.git
`

Then, install requirements using nonebot-cli (nb). (Don't use requirements.txt)

`
nb create
`

(Only create a blank project, use global install)

After all actions, edit `.env.prod` `.env.dev` `bot.py` 'SUPERUSER' configure section to your qq Number.

Then, open `data/configuration_template.json`, edit `AI-ApiKEY`. Rename it to `data/configuration.json`
If you do not need AI skill, just `data/configuration_template.json` to `data/configuration.json` is best choice.

Run `nb run --reload` to boot this bot.

## How to connect bot to QQ?

Go https://github.com/NapNeko/NapCatQQ.
