import argparse
import os


from bs4 import BeautifulSoup
from openai import OpenAI
import requests

parser = argparse.ArgumentParser(description='Program to take a URL and get some questions to ask back')
parser.add_argument('url',  type=str,
                    help='A URL to get questions about')

parser.add_argument('--number-of-questions', dest='number_of_questions',  type=int, default=3,
                    help='number of questions to ask')

args = parser.parse_args()

response = requests.get(args.url)
soup = BeautifulSoup(response.content, features="html.parser")
url_body = soup.get_text()

prompt = f"""For the following text could you reply with a list of {args.number_of_questions} 
questions I could ask to someone to see if they have understood it: '{url_body}'"""

client = OpenAI()
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)

if True:
    print("*** Copying to system clipboard!")
    os.system(f'echo "{chat_completion.choices[0].message.content}" | pbcopy')


