import argparse
import os

from bs4 import BeautifulSoup
from openai import OpenAI
import requests

if __name__ == "__main__":
    # Parse args from command line, needs a URL but everything else is optional
    parser = argparse.ArgumentParser(description='Program to take a URL and get some questions to ask back')
    parser.add_argument('url',  type=str,
                        help='A URL to get questions about')

    parser.add_argument('--number-of-questions', dest='number_of_questions',  type=int, default=3,
                        help='number of questions to ask')

    parser.add_argument('--clipboard', dest='copy_to_clipboard',  type=bool, default=False,
                        help='should auto copy to clipboard')
    args = parser.parse_args()

    # Get the data from the URL and just get all the text from the page
    # IDEALLY would do something slightly more clever here
    response = requests.get(args.url)
    soup = BeautifulSoup(response.content, features="html.parser")
    url_body = soup.get_text()

    # Construct the prompt for GPT and then send
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

    # Print the response
    print(chat_completion.choices[0].message.content)

    if args.copy_to_clipboard:
        print("*** Copying to system clipboard!")
        os.system(f'echo "{chat_completion.choices[0].message.content}" | pbcopy')

