import os
import json
import requests
import openai

app_id = os.getenv("MATHPIX_APP_ID")
app_key = os.getenv("MATHPIX_APP_KEY")
open_ai_key = os.getenv("OPEN_API_KEY")
          

testMathpix = "{'request_id': '2023_05_26_68e6c1a4d37d79573a2eg', 'version': 'RSK-M115', 'image_width': 2652, 'image_height': 568, 'is_printed': True, 'is_handwritten': False, 'auto_rotate_confidence': 0, 'auto_rotate_degrees': 0, 'confidence': 1, 'confidence_rate': 1, 'latex_styled': '\\begin{aligned}\nP\\left(X=x \\mid Y=c_{k}\\right) & =P\\left(X^{(1)}=x^{(1)}, \\cdots, X^{(n)}=x^{(n)} \\mid Y=c_{k}\\right) \\\\\n& =\\prod_{j=1}^{n} P\\left(X^{(j)}=x^{(j)} \\mid Y=c_{k}\\right)\n\\end{aligned}', 'text': 'rm_spaces\\begin{aligned} P\\left(X=x \\mid Y=c_{k}\\right) & =P\\left(X^{(1)}=x^{(1)}, \\cdots, X^{(n)}=x^{(n)} \\mid Y=c_{k}\\right) \\\\ & =\\prod_{j=1}^{n} P\\left(X^{(j)}=x^{(j)} \\mid Y=c_{k}\\right)\\end{aligned}true'}"
resultstr= "\\begin{aligned}\nP\\left(X=x \\mid Y=c_{k}\\right) & =P\\left(X^{(1)}=x^{(1)}, \\cdots, X^{(n)}=x^{(n)} \\mid Y=c_{k}\\right) \\\\\n& =\\prod_{j=1}^{n} P\\left(X^{(j)}=x^{(j)} \\mid Y=c_{k}\\right)\n\\end{aligned}"
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
    response = requests.post(url, headers=headers, json=json)
    result = response.json()
    # print(json.dumps(result, indent=4, sort_keys=True))
    print(result['latex_styled'])
    return result['latex_styled']


def get_ai_response(formula):
    prompt = (f"请解释这个 LaTeX 公式的含义: {formula}\\n"
          f"每个参数的含义是什么?")
    message = get_completion(prompt)
    return message


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]