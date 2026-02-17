import json
import requests
import os
from dotenv import load_dotenv

class LLMBridge:
    def __init__(self):
        # 自动搜索并加载根目录下的 .env 文件
        load_dotenv()
        
        # 从环境变量中读取配置
        self.api_key = os.getenv("AMI_LLM_API_KEY")
        self.api_url = os.getenv("AMI_LLM_URL", "https://api.deepseek.com/chat/completions")

        if not self.api_key:
            raise ValueError("错误：未找到 API Key。请在根目录 .env 文件中配置 AMI_LLM_API_KEY。")

    def ask(self, prompt):
        """
        核心能力：将语义转化为结构化 JSON。
        严格约束：仅准许返回符号库中存在的 Canonical Symbols 序列。
        """
        system_prompt = (
            "你是一个精准的符号拆解器。你必须且只能返回 JSON。\n"
            "可选符号池：[REF_SELF, REF_USER, NEGATIVE, POSITIVE, BODY, KNOWLEDGE, ACTION_SING, OBJ_SONG]\n"
            "禁止在 response_symbols 中包含任何自然语言词汇。"
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=15)
            response.raise_for_status() # 检查 HTTP 响应状态
            result = response.json()
            content = result['choices'][0]['message']['content']
            return json.loads(content)
        except Exception as e:
            # 保持 Ammie 的健壮性，返回错误详情供审计
            return {"intent": "UNKNOWN", "error": str(e)}