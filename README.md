# ToolsBot

## 如何部署

1. 打开 Python 命令行,输入以下命令:
Windows:

```
pip install pipx
start cmd
```
在新窗口中输入:
```
pipx install nb-cli
pipx ensurepath
start cmd
```
再在新窗口中输入:
```
git clone https://gitee.com/DKoTechnology/tools-bot.git

python -m venv .venv

nb create
```
输入名称 自定义
适配器选 Onebot 和 Console, 如果后面跑不了就看依赖中有cqhttp的都删了
其他的都自定义
搞完後把 clone 下载的文件和文件夹都复制到新文件夹里,然后删掉除这个新文件夹外的所有内容
```
nb run --reload
```
机器人,启动!

## 配置 QQ
我们都知道 OpenShamrock 和 LiteloaderNTQQ,我推荐 LiteLoaderNTQQ.
以下是如何配置.

下载 NTQQ,然后 clone 下载 LiteloaderNTQQ,按照官方文档配置.
随后下载 LLOnebot,安装.
打开设置,配置一下 反向 Websocket. 这个看官方 Onebot 文档.

随后保存,你应该可以看到 Console 适配器里已经输出了连接信息.

##### 开始使用吧!

