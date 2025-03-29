import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyATXjrPAriE7QUzFr6tYcP2iOrnaM9pioc")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

text = ""
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

  if content_div:
    return f"{content_h1.text}\n\n{content_div.text}"
  else:
    return ""

text = get_content_from_url("https://m.shuhaige.net/375928/129589886.html")

print("Url fetched successfully.")

prompt = f"""
I will provide you html element with chinese content. You have get the content from the element and translate into english. Then return the final translated content.
HTML Element: {text}
"""
response = model.generate_content(prompt)

with open('example.md', 'w', encoding='utf-8') as file:
  file.write(response.text.replace('  ', ' '))
