import json
import requests
from django.conf import settings

API_KEY = settings.TALKBOT_API_KEY
URL = "https://api.talkbot.ir/v1/chat/completions"

def get_model_response(prompt, model="gpt-4-turbo"):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    payload = json.dumps({
        "model": model,
        "messages": prompt,
        "max_tokens": 2000,
        "temperature": 0.2,
        "top_p": 0.9
    })

    response = requests.post(URL, data=payload, headers=headers)
    if response.ok:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"
