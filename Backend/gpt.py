import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY= "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"
openai.api_key = OPENAI_API_KEY

messages = [
            {"role": "system", "content": "You are a medicl professional that can diagnose patients."},
            ]
print("---Welcome to Terminal-GPT---")
print('---Type "quit" to exit---')

while (True):
    # Get user input
    print("")
    user_input = input("Enter query: ")
    if user_input == "":
        continue
    if user_input == "quit":
        break

    messages.append({"role": "user", "content": user_input})
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )

    messages.append(response.choices[0].message)
    print("\n" + response.choices[0].message.content)

    if (response.choices[0].finish_reason != "stop"):
        print("\nYou've exceeded the max supply of tokens. Please restart the program.")
        break

def get_gpt_response(input):
    pass