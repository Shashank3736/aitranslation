import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyATXjrPAriE7QUzFr6tYcP2iOrnaM9pioc")
model = genai.GenerativeModel("gemini-2.0-flash")

safetySettings = [
    {
      "category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_NONE,
    },
    {
      "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_NONE,
    },
    {
      "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_NONE,
    },
    {
      "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_NONE,
    },
  ];

def get_content_from_url(url):
  response = requests.get(url)
  response.encoding = 'utf-8'
  soup = BeautifulSoup(response.text, 'html.parser')
  content_div = soup.find('div', class_='content')
  content_h1 = soup.find('h1', class_='headline')
  content_body = soup.find('body')

  return content_body
  # if content_div:
  #   return f"{content_h1.text}\n\n{content_div.text}"
  # else:
  #   return ""

text = get_content_from_url("https://m.shuhaige.net/375928/129589887.html")

def translate_using_ai(text, target_language, source_language):
  prompt = f"""
  I will provide you html element with {source_language} content. You have get the content from the element and translate into {target_language}. Then return the final translated content.
  HTML Element: {text}
  """
  
  response = model.generate_content(prompt)
  return response.text

def translate_body(text, target_language, source_language):
  prompt = f"""
  I will provide you html body you have to do these stuff. you have to return 3 stuff in json format.

  1. "next_chapter": Next chapter url parameter

  2. "chapter_title": Chapter title translated in {target_language}

  3. "chapter_content": Chapter content translated in {target_language}
  
  HTML Body: {text}
  """

  response = model.generate_content(prompt)
  print(response.text)
  try:
    json_data = json.loads(response.text.replace("```json", "").replace("```", ""))
    return json_data
  except json.JSONDecodeError:
    return {"error": "Invalid JSON format"}


if __name__ == "__main__":

  with open('example.md', 'w', encoding='utf-8') as file:
    file.write(translate_body(text, "English", "Chinese")["chapter_content"].replace("\n", "\n\n"))
