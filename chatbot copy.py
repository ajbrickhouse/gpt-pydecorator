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
import pandas as pd
import warnings

# Load the API key from .env file
load_dotenv()
def default(o):
    if isinstance(o, datetime):
        return o.__str__()
    return str(o)  # Ensure content is always a string

json.JSONEncoder.default = default

openai.api_key = "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"
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


@openaifunc
def search_master_list(keyword: str) -> dict:
    """
    Searches the master list for any keyword and returns all of the information related to the matches
    @param keyword: The keyword to search for
    """
    print("Searching master list for keyword: " + keyword)
    file_path = 'ACvFLO master list.xlsx'

    try:
        xls = pd.ExcelFile(file_path)
    except ValueError as e:
        print(f"Error reading the file: {e}")
        return {}

    result = {}

    for sheet_name in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name)
        except Exception as e:
            print(f"Error reading sheet '{sheet_name}': {e}")
            continue

        # Filter the DataFrame for rows containing the keyword
        matching_rows = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]

        if not matching_rows.empty:
            # Convert the filtered DataFrame to a list of rows
            result[sheet_name] = matching_rows.values.tolist()
    # print(result)
    return result

@openaifunc
def search_master_schedule(keyword: str) -> dict:
    """
    Searches the master schedule for any keyword and returns all of the information related to the matches
    @param keyword: The keyword to search for
    """
    print("Searching master schedule for keyword: " + keyword)
    try:
        df = pd.read_excel('Master Schedule.xlsx', sheet_name='Master Schedule')
    except Exception as e:
        print(f"Error reading the file: {e}")
        return {}

    result = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]
    # print(result.to_dict(orient='list'))
    return result.to_dict(orient='list')

@openaifunc
def search_all_masters(keyword: str) -> dict:
    """
    Searches the master list and master schedule for any keyword and returns all of the information related to the matches
    @param keyword: The keyword to search for
    """
    print("Searching master list and master schedule for keyword: " + keyword)
    result = {}
    try:
        master_list_results = search_master_list(keyword)
        result["Master List"] = master_list_results
    except Exception as e:
        print(f"An error occurred while searching the master list: {e}")

    try:
        master_schedule_results = search_master_schedule(keyword)
        result["Master Schedule"] = master_schedule_results
    except Exception as e:
        print(f"An error occurred while searching the master schedule: {e}")

    return result

# ChatGPT API Function
def send_message(message, messages, model_arg="gpt-4-1106-preview"):
    messages.append(message)

    # Convert the 'content' of each message to a string if it is not already
    for msg in messages:
        if isinstance(msg.get('content'), dict):
            msg['content'] = json.dumps(msg['content'], default=str)

    try:
        response = openai.ChatCompletion.create(
            model=model_arg,
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

        await message.channel.send("Working on it...")

        messages = []  # Initialize messages as an empty list
        messages = send_message({"role": "user", "content": message.content}, messages)
        
        # # Get ChatGPT response
        # chatgpt_response = messages[-1]["content"]

        # If ChatGPT response is a function call, call the function
        if messages[-1].get("function_call"):
            function_name = messages[-1]["function_call"]["name"]
            arguments = json.loads(messages[-1]["function_call"]["arguments"])

            if function_name in globals() and callable(globals()[function_name]):
                # if function_name == "keyword_search_excel":
                #     keyword = arguments.get("keyword")
                #     if keyword:
                #         function_response = globals()[function_name](keyword)
                #     else:
                #         print("Keyword argument is missing for keyword_search_excel")
                #         await message.channel.send("Error: Keyword argument is missing.")
                #         return  # Exit the function early
                # else:
                function_response = globals()[function_name](**arguments)

                print(f"Function '{function_name}' called with arguments: {arguments}")
                print(f"Function response: {function_response}")

                # Send function result back to ChatGPT
                messages = send_message(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": "Please provide a detailed outline about this data: " + function_response,
                    },
                    messages,
                    "gpt-3.5-turbo-1106",
                )

        # Get the final response from ChatGPT
        final_response = messages[-1]["content"]

        # Send final response to Discord
        await message.channel.send(final_response)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
asyncio.run(client.start_bot())