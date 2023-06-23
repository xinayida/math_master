import os
import json
import requests
import openai
import logging

GPT_MODEL = "gpt-3.5-turbo-0613"
app_id = os.getenv("MATHPIX_APP_ID")
app_key = os.getenv("MATHPIX_APP_KEY")
openai.api_key  = os.getenv("OPEN_API_KEY")
openai.proxy = "http://127.0.0.1:7890"

def get_mathpix_response(img):
    url = 'https://api.mathpix.com/v3/text'
    image_file = 'test.jpg'
    options_json = '{"math_inline_delimiters": ["$", "$"], "rm_spaces": true}'

    headers = {
        'app_id': app_id,
        'app_key': app_key
    }
    # files = {
    #     'file': open(image_file, 'rb')
    # }
    json = {
        "src": img,
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
    }
    try:
        response = requests.post(url, headers=headers, json=json)
        if response.status_code == 200:
            result = response.json()
            # print(json.dumps(result, indent=4, sort_keys=True))
            return (200, result['latex_styled'])
        else:
            return (response.status_code, "Request Failed")
    except requests.exceptions.RequestException as e:
        return (0, str(e))

def get_ai_title(formula):
    formatStr = formula.replace("\\", "\\\\").strip('\"\"\"')
    prompt = (f"请用中文回复<>中包含的公式的名称是什么? Please return the answer without embellish and punctuation mark. If it's not formula reply 'None' directly. ``` <{formatStr}> ```")
    logging.info(f"call openai API for title ...")
    message = get_completion(prompt)
    logging.info(message)
    return message

def get_ai_explain(formula):
    prompt = (f"请解释这个 LaTeX 公式的含义: <{formula}>\\n"
              f"并解释每个参数的含义是什么?")
    logging.info("call openai API for explain ...")
    message = get_completion(prompt)
    logging.info(message)
    return message


def get_completion(prompt, model=GPT_MODEL):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    except requests.exceptions.RequestException as e:
        return (0, str(e))