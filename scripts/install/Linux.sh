#!/bin/bash

# 在安装所有依赖前，必须先创建虚拟环境。
echo ":: 正在创建虚拟环境..."
python -m venv ../.venv

# 加载虚拟环境
source ../.venv/bin/activate

# pipx
echo ":: 正在安装 pipx..."
python -m pip install pipx

# pipx nbcli
echo ":: 正在安装 nonebot cli..."
pipx install nb-cli

# pipx ensurepath
echo ":: 正在准备 Path..."
pipx ensurepath

# pip install requirements
echo ":: 正在安装 Bot 依赖..."
pip install -r ./requirements.txt

echo ":: Bot 依赖和基本框架安装完毕。"