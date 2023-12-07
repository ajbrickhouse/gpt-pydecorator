#!/usr/bin/env python3
from openai_decorator.openai_decorator import openaifunc, get_openai_funcs

import openai
import os
import sys
import json
from dotenv import load_dotenv
import openpyxl
from datetime import datetime
import discord
import asyncio

# Load the API key from .env file
load_dotenv()
def default(o):
    if isinstance(o, datetime):
        return o.__str__()
    return str(o)  # Ensure content is always a string

json.JSONEncoder.default = default

openai.api_key = "sk-FdCrfAucoEQk9J0cdXqxuT3BlbkFJM1HsMjeNtK9vnsnzgztX"

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

class MyClient(discord.Client):
    async def start_bot(self):
        while True:
            try:
                await self.start(os.getenv("DISCORD_TOKEN"))
            except discord.errors.ConnectionClosed as e:
                print(f"Connection closed: {e}, attempting to reconnect in 5 seconds.")
                await asyncio.sleep(5)  # wait before reconnecting
            except Exception as e:
                print(f"Unexpected error: {e}")
                break  # Exit the loop if the error is not related to connection

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return  # Avoid responding to the bot's own messages

        messages = []  # Initialize messages as an empty list
        messages = send_message({"role": "user", "content": message.content}, messages)
        
        # Get ChatGPT response
        chatgpt_response = messages[-1]["content"]

        # If ChatGPT response is a function call, call the function
        if messages[-1].get("function_call"):
            function_name = messages[-1]["function_call"]["name"]
            arguments = json.loads(messages[-1]["function_call"]["arguments"])

            if function_name in globals() and callable(globals()[function_name]):
                if function_name == "keyword_search_excel":
                    keyword = arguments.get("keyword")
                    if keyword:
                        function_response = globals()[function_name](keyword)
                    else:
                        print("Keyword argument is missing for keyword_search_excel")
                        await message.channel.send("Error: Keyword argument is missing.")
                        return  # Exit the function early
                else:
                    function_response = globals()[function_name](**arguments)

                # Send function result back to ChatGPT
                messages = send_message(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    },
                    messages,
                )

            # Get the final response from ChatGPT
            final_response = messages[-1]["content"]

            # Send final response to Discord
            await message.channel.send(final_response)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
asyncio.run(client.start_bot())