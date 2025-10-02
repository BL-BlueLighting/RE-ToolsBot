import requests, json

api_key = "sk-quhtfffmcbqsmlfsrpjgpowkkhprnkrqrpwqnyqzjybfuxzn"

payload = {
    "model": "Qwen/Qwen3-8B",
    "messages": [
        {
            "role": "system",
            "content": "你是一个名叫 ToolsBot 的 Bot。现在是 2025 年。接下来用户会给你发送消息，请直接发送结果并使用简洁的语言。"
        },
        {
            "role": "user",
            "content": "你好"
        }
    ]
}

headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json"
}


response = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers).content
# 获取返回的内容
js_resp = json.loads(response)
print(js_resp)

# choices
choices = js_resp.get("choices")
print(choices)

# message
messag_ = choices [0].get("message")
print(messag_)

# content
ctnt = messag_.get("content")

# usage
usage = js_resp.get("usage")

# total token
total_token = usage.get("total_tokens")

msg = f"""ToolsBot AI
- 模型:    Qwen\\Qwen3-8B
- 回复内容：
    {ctnt}
- 此次扣除金额：{total_token}
"""