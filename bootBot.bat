@echo off
chcp 65001
REM 检测是否存在虚拟环境
where poetry >nul 2>nul
if %errorlevel% equ 0 (
    echo 检测到poetry, 使用虚拟环境
    poetry run nb run --reload
) else (
    echo poetry不存在, 直接运行
    nb run --reload
)
echo Robot was finished.
pause