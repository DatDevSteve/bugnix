import os
from openai import AzureOpenAI
from dotenv import load_dotenv

endpoint = "https://rehaa-m9ctl9bk-eastus2.cognitiveservices.azure.com/"
model_name = "o3-mini"
deployment = "o3-mini"

load_dotenv()
subscription_key = os.getenv("AZURE_OPENAI_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

with open("app/handlers/bugnix_context.txt", "r") as f:
    context = f.read()

#hardcoded error:
error_text = """Traceback (most recent call last):
  File "/mnt/.../main.py", line 3, in <module>
    from app.handlers.ocr_handler import extract_text
  File "/mnt/.../ocr_handler.py", line 24
    ^
SyntaxError: expected 'except' or 'finally' block""" 

def analyse_error(error):
    try:
        response = client.chat.completions.create(
        stream=True,
        messages=[
            {"role": "system", "content": f'{context}' },
            {"role": "user", "content": f'Please provide a solution to this error {error}'}
        ],
        max_completion_tokens=100000,
        model=deployment,
        )

        for update in response:
            if update.choices:
                print(update.choices[0].delta.content or "", end="")
    except Exception as e:
        return f'[!] Fatal Error in LLM Module: {e} '
    
    


analyse_error(error_text)