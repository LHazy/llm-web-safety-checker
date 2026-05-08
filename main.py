import os
import sys
import base64
import argparse
import datetime

from dataclasses import dataclass

from io import BytesIO
from PIL import Image

from langchain.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def image_to_base64(file_path):
  pi = Image.open(file_path)
  buffer = BytesIO()
  pi.save(buffer, format="PNG")
  img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
  return img_str


def take_screenshot(url):
  options = Options()
  options.add_argument('--headless=new')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--window-size=1080,720')
  
  now = datetime.datetime.now()
  filename = f'screenshot_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.png'

  chromedriver_path = "/usr/bin/chromedriver"
  service = Service(chromedriver_path)
  
  driver = webdriver.Chrome(service=service, options=options)
  driver.get(url)

  width = driver.execute_script('return document.body.scrollWidth')
  height = driver.execute_script('return document.body.scrollHeight')
  driver.set_window_size(width, height)

  save_path = f'./screenshots/{filename}'
  driver.save_screenshot(save_path)
  driver.quit()

  return save_path


judge_prompt = '''
スクリーンショットを読み込んでWebサイトの安全性を評価してください。
回答は以下のJSONを出力してください。
* 安全な場合
{
  "result": "safe"
}
* 安全でない場合
{
  "result": "unsafe",
  "reason": "危険な要素の説明"
}
'''

def judge_safe(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(image_part)
    content_parts.append(text_part)

    return [HumanMessage(content=content_parts)]


def main(model_endpoint, model_id, url):
  file_path = take_screenshot(url)
  image_b64 = image_to_base64(file_path)
  
  llm = ChatOllama(
    model=model_id,
    base_url=model_endpoint,
    api_key="ollama",
    #reasoning="high",
    #num_ctx=1024*128,
    temperature=0
  )
  
  chain = judge_safe | llm | StrOutputParser()
  query_chain = chain.invoke({"text": judge_prompt, "image": image_b64})
  
  print(query_chain)


if __name__ == "__main__":
  """
  Usage: python main.py --model-endpoint http://host.docker.internal:11434/ --model-id gemma4:31b <url>
    - --model-endpoint: Endpoint of the LLM server (default: http://host.docker.internal:11434/)
    - --model-id: ID of the model to use (default: gemma4:31b)
    - <url>: URL of the website to check
  """
  parser = argparse.ArgumentParser(description='LLM Web Safety Checker')
  parser.add_argument('--model-endpoint', type=str, default='http://host.docker.internal:11434/', help='Endpoint of the LLM server')
  parser.add_argument('--model-id', type=str, default='gemma4:31b', help='ID of the model to use')
  parser.add_argument('url', type=str, help='URL of the website to check')
  args = parser.parse_args()

  if not os.path.exists('./screenshots'):
    os.makedirs('./screenshots')
  
  url = args.url
  model_endpoint = args.model_endpoint
  model_id = args.model_id
  main(model_endpoint, model_id, url)
