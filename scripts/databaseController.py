import json
import sqlite3

print("RE: ToolsBot - SQLite3 命令行 - EASY\n该命令行过于简陋，请最好使用 SQLite Browser 等 SQLite 专业浏览器。")
print("请先稍等，正在打开链接...")

conn = sqlite3.connect("../userdata.db")
cursor = conn.cursor()

print("userdata.db - 链接打开成功。\n")

while True:
    try:
        sql = input("> ")
        if sql == "exit":
            print("Goodbye.")
            conn.close()
            break

        cursor.execute(sql)
        # 解析
        for row in cursor.fetchall():
            print(row)
        conn.commit()

    except KeyboardInterrupt:
        print("Goodbye.")
        conn.close()
        break

    except Exception as e:
        print("Error: " + e.__str__())
        continue;