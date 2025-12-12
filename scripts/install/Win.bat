@echo off

echo :: 正在安装 pipx...
start cmd /k pip install pipx && exit

echo :: 正在安装 nb-cli...
start cmd /k pipx install nb-cli && exit

echo :: 正在运行 ensurepath...
start cmd /k pipx ensurepath && exit

echo :: 正在安装 Bot 所需依赖...
pip install -r ./requirements.txt

echo :: 安装结束。