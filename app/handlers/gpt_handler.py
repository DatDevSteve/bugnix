#LLM MODULE FOR PERFORMING CODE INTERPRETATION
#USES AZURE OPEN AI WITH GPT o3 MINI

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

#Instance Configuration:
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

#Setup Context for the AI Agent:
with open("app/handlers/bugnix_context.txt", "r", encoding="utf-8") as f:
    context = f.read()

#Analysis Function:
def analyze_error(error):
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
        #Generator for streaming output in chunks, used to dynamically give a generative effect to output:
        for update in response:
            if update.choices:
                chunk = update.choices[0].delta.content or ""
                yield chunk
    
    except Exception as e:
        yield f'[!] Fatal Error in LLM Module: {e} '
    
