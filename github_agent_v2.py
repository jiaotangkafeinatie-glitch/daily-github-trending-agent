import requests
from openai import OpenAI
import json
import os
from datetime import datetime

# 1. 基础配置
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=d38df22c13714a56df0a17fd56b05a592a83b89780645b1aa4c1bd0d867e6c16"
client = OpenAI(
    api_key="sk-a6d03b1fc88a4f53a89e2ac09f4068a4", 
    base_url="https://api.deepseek.com"
)
JSON_FILE = "history.json"

# 2. 记忆模块：读写 JSON
def load_memory():
    """读取 JSON 数据库，如果不存在或报错则返回空字典"""
    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_to_memory(name, description, analysis):
    """保存结构化数据：包含项目名、原始描述、AI评价和时间"""
    memory = load_memory()
    memory[name] = {
        "description": description,
        "ai_analysis": analysis,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        # ensure_ascii=False 保证中文不乱码，indent=4 让文件整齐
        json.dump(memory, f, ensure_ascii=False, indent=4)

# 3. 抓取逻辑（使用你之前跑通的官方接口）
def get_trending():
    print("🌐 正在连接 GitHub 实时数据...")
    url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars"
    try:
        res = requests.get(url, timeout=10)
        return res.json()['items'][:5]
    except:
        print("❌ 网络波动，使用离线演示模式...")
        return [{"full_name": "test/demo", "description": "这是一个测试项目"}]
        

def send_to_dingtalk(content):
    """把 AI 的分析结果推送到钉钉"""
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": f"【GitHub 趋势日报】\n\n{content}"
        }
    }
    # 发送网络请求给钉钉
    try:
        res = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            print("🚀 消息已成功推送到手机！")
    except:
        print("❌ 推送失败，请检查网络。")

def ai_analyze(name, desc):
    """这是 AI 的大脑部分"""
    prompt = f"项目名：{name}\n描述：{desc}\n\n请用一句话解释这是做什么的，并给出推荐理由。"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 暂时短路了: {e}"

# 4. 主程序
if __name__ == "__main__":
    memory = load_memory()
    projects = get_trending()
    
    report_list = [] # 用来收集今天要发的消息内容
    
    for p in projects:
        name = p['full_name']
        if name in memory:
            continue
            
        analysis = ai_analyze(name, p['description'])
        save_to_memory(name, p['description'], analysis)
        
        # 把新项目的信息拼接到报告列表里
        report_list.append(f"📌 项目: {name}\n💡 AI评价: {analysis}")

    # 如果有新项目，一次性推送到钉钉
    if report_list:
        final_report = "\n\n".join(report_list)
        send_to_dingtalk(final_report)
    else:
        print("今天没有新项目，不打扰你了。")