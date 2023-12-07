#!/usr/bin/env python3
from openai_decorator.openai_decorator import openaifunc, get_openai_funcs

import openai
import os
import sys
import json
from dotenv import load_dotenv
import openpyxl
from datetime import datetime

# Load the API key from .env file
load_dotenv()
openai.api_key = "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"

# Convert datetime object to string
def default(o, *args):
    if isinstance(o, datetime):
        return o.__str__()

json.JSONEncoder.default = default

@openaifunc
def keyword_search_excel(keyword) -> dict:
    """
    Searches the master list for any keyword and returns all of the information related to the matches
    """
    wb = openpyxl.load_workbook('ACvFLO master list.xlsx')
    result = {}

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        rows = []

        for row in sheet.iter_rows(values_only=True):
            if keyword in row:
                rows.append(row)

        if rows:
            header = [cell.value for cell in sheet[1]]
            rows.insert(0, header)

        result[sheet_name] = rows

    return result

@openaifunc
def recommend_youtube_channel() -> str:
    """
    Gets a really good recommendation for a YouTube channel to watch
    """
    return "Unconventional Coding"

@openaifunc
def calculate_str_length(string: str) -> str:
    """
    Calculates the length of a string
    """
    return str(len(string))

# ChatGPT API Function
def send_message(message, messages):
    messages.append(message)

    # Convert the 'content' of each message to a string if it is not already
    for msg in messages:
        if isinstance(msg.get('content'), dict):
            msg['content'] = json.dumps(msg['content'], default=str)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=messages,
            functions=get_openai_funcs(),
            function_call="auto",
        )
    except openai.error.OpenAIError as e:
        print(f"OpenAIError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)

    messages.append(response["choices"][0]["message"])
    return messages



# MAIN FUNCTION
def run_conversation(prompt, messages=[]):
    # add user prompt to chatgpt messages
    messages = send_message({"role": "user", "content": prompt}, messages)

    # get chatgpt response
    message = messages[-1]

    # loop until project is finished
    while True:
        if message.get("function_call"):
            # get function name and arguments
            function_name = message["function_call"]["name"]
            arguments = json.loads(message["function_call"]["arguments"])

            # call function dangerously
            if function_name == "get_current_weather":
                function_response = globals()[function_name](arguments.get("location"), arguments.get("country"))
            else:
                function_response = globals()[function_name](**arguments)

            # send function result to chatgpt
            messages = send_message(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
                messages,
            )
        else:
            # if chatgpt doesn't respond with a function call, ask user for input
            print("ChatGPT: " + message["content"])

            user_message = input("You: ")

            # send user message to chatgpt
            messages = send_message(
                {
                    "role": "user",
                    "content": user_message,
                },
                messages,
            )

        # save last response for the while loop
        message = messages[-1]

# ASK FOR PROMPT
print(
    "Go ahead, ask for the weather, a YouTube channel recommendation or to calculate the length of a string!"
)
prompt = input("You: ")

# RUN CONVERSATION
run_conversation(prompt)
