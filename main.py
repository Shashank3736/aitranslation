import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyATXjrPAriE7QUzFr6tYcP2iOrnaM9pioc")
model = genai.GenerativeModel("gemini-1.5-flash")

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
with open('input.txt', 'r', encoding='utf-8') as input_file:
    text = input_file.read()
prompt = f"""
Translate the following Japanese text into English. Ensure the translation is accurate, natural, and maintains the original meaning and tone. If the text includes cultural nuances or idioms, provide an explanation or equivalent expression in English.

Japanese text: {text}

Translated English text:
"""
response = model.generate_content(prompt, safety_settings=safetySettings)

with open('example.md', 'w', encoding='utf-8') as file:
    # print(response.text)
    file.write(response.text.replace('  ', ' ').replace("\n\n", "\n"))
