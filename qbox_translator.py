import argparse
import logging
from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)
# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 远程翻译服务的 URL
URL = "http://127.0.0.1:11434/api/generate"


@app.route("/translate", methods=["POST"])
def translate():
    # 1.智能体第一步：环境识别，即接收浏览器插件的翻译请求
    # 记录请求头信息
    logging.info(f"Request Headers: {dict(request.headers)}")
    # 记录请求体信息
    logging.info(f"Request Body: {request.json}")
    # 从请求头提取 API 密钥
    provided_key = request.headers.get("Authorization")
    if not provided_key or provided_key != f"Bearer {API_KEY}":
        logging.warning("Unauthorized request received")
        return Response("Invalid API Key", status=403)
    # 获取用户请求中的翻译内容
    data = request.json
    text_to_translate = data.get("prompt", "")
    model_origin = data.get("model", "")
    print('data:\n', data)
    # 2.智能全体第二步：编排，即封装提示词，并向本地LLM模型请求翻译
    if prompt_from_origin == 0:
        # 修改插件提供的提示词（Translate the following text from Auto-detect to Simplified Chinese:\n\nMultilingual
        # capabilities）：Translate the following text to Simplified Chinese and return only the translation:
        # "Multilingual capabilities"
        # 解析文本，确保不会因索引错误导致崩溃
        text_parts = text_to_translate.split("\n\n")
        print('--->', text_parts)
        if len(text_parts) > 1:
            text_to_translate = f"Translate the following text to Simplified Chinese and return only the direct " \
                                f"translation, without any explanations or breakdowns: \n\n{text_parts[1]} "
        else:
            text_to_translate = f"Translate the following text to Simplified Chinese and return only the direct " \
                                f"translation, without any explanations or breakdowns: \n\n{text_to_translate} "
    if not text_to_translate:
        logging.error("Missing text parameter in request")
        return Response("Missing text parameter", status=400)
    if model_local != '':
        model = model_local
    else:
        model = model_origin
    # 构建请求数据
    payload = {
        "model": model,
        "prompt": text_to_translate,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    print('payload:\n', payload)
    try:
        # 发送请求到远程翻译服务，并设置超时时间
        response = requests.post(URL, data=json.dumps(payload), headers=headers, timeout=50)

        # 智能体第三步：LLM决策，即本地LLM模型返回翻译结果，将结果返回给浏览器插件
        # 直接返回请求结果，不做任何包装
        return Response(response.content, status=response.status_code,
                        content_type=response.headers.get("Content-Type", "application/json"))
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
        return Response("Request timed out", status=504)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return Response(f"Request failed: {str(e)}", status=500)


# 解析命令行参数
parser = argparse.ArgumentParser(description="启动 Flask 服务器")
parser.add_argument("-m", type=str, default="", help="强制指定模型 model_local（默认: 空字符串）")
parser.add_argument("-pf", type=int, default=0, help="是否自定义提示词 prompt_from_origin（默认: 0）")
parser.add_argument("-p", type=int, default=6500, help="指定端口号（默认: 6500）")
parser.add_argument("-k", type=str, default="qbox_qhub", help="指定api_key（默认: qbox_qhub）")
args = parser.parse_args()
# 赋值参数
model_local = args.m
prompt_from_origin = args.pf
port = args.p
# 设定 API 密钥（用于身份验证）
API_KEY = args.k
# 以简洁格式打印参数信息
print(f"-m: 强制指定模型 {model_local}（默认: ''）")
print(f"-pf: 是否自定义提示词 {prompt_from_origin}（默认: 0）")
print(f"-p: 指定服务端口号{port}（默认: 6500）")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
