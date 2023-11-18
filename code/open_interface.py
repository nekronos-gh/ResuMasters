from openai import AzureOpenAI
import json
import os, sys


def load_api_keys_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            api_keys = json.load(json_file)
            for key, value in api_keys.items():
                os.environ[key] = value
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit()
    except json.JSONDecodeError:
        print(f"Error parsing JSON in '{file_path}'.")
        sys.exit()

def ask_gpt(text_query):
    client = AzureOpenAI(
        api_version="2023-07-01-preview",
        azure_endpoint=os.environ.get("AZURE_ENDPOINT")
    )
    return  client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"{text_query}"}]
                ).choices[0].message.content

def do_dall_e(text_query):
    client = AzureOpenAI(
        api_version="2023-07-01-preview",
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_ENDPOINT")
    )
    return  client.images.generate(
                model="dalle3",
                prompt=text_query,
                size="1024x1024",
                quality="standard",
                n=1
                ).data[0].url

def ask_gpt_context(text_query, context=""):
    client = AzureOpenAI(
        api_version="2023-07-01-preview",
        azure_endpoint=os.environ.get("AZURE_ENDPOINT")
    )
    return  client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"<previous_context>{context}</previous_context>\nHuman: {text_query}\nChatGPT:"}]
                ).choices[0].message.content
