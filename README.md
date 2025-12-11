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

<p align="center"><i>Perfect Bot for QQ.</i></p>

## How to use it?
First, clone this project.

`
git clone https://github.com/Latingtude/RE-ToolsBot.git
`

Choose one of the following two actions

<details>
<summary>Install dependencies(Main Environment)</summary>
Install requirements using this python script:

`
python ./installTB.py
`

Or, install requirements directly

`
pip install -r ./install/requirements.txt
`

</details>

<details>
<summary>Install dependencies(Virtual Environment)</summary>
1.Install Python version 3.10 or higher

2.Run `pip install poetry`

3.Run `poetry install`

(Note: Are there really people who would want to deploy this project in the main environment?)

</details>

(Only create a blank project, use global install)

After all actions, edit `.env.prod` `.env.dev` `bot.py` 'SUPERUSER' configure section to your qq Number.

Then, open `data/configuration_template.json`, edit `AI-ApiKEY`. Rename it to `data/configuration.json`
If you do not need AI skill, just `data/configuration_template.json` to `data/configuration.json` is best choice.

Run `nb run --reload` to boot this bot.

## How to connect bot to QQ?

Go https://github.com/NapNeko/NapCatQQ.

## Thanks
> [!Note]
>
> Thanks for project under. I used some code from them.

<a href="https://github.com/yzyyz1387/nonebot_plugin_admin/">NoneBot Plugin Admin</a>

## Tips
> [!Warning]
>
> This project is **not** stable.
>
> Please don't direct clone this repo.
>
> I can't do check my code anytime.
>
> If you found a issue, please make a issue context in `Github Issues` !