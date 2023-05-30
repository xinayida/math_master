from pprint import pprint
from utils import downloadImage
import configparser
import requests
import json
import logging

config = configparser.ConfigParser()
config.read('config.ini')  # 读取本地配置文件
token = config.get("notion","NOTION_KEY")
db_id = config.get("notion", "NOTION_DB_ID")

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

url = "https://api.notion.com/v1/pages"

##根据title查询页面
def queryPage(title) -> dict:
    searchUrl = "https://api.notion.com/v1/search"
    queryData = {
        "query":title,
            "filter": {
            "value": "page",
            "property": "object"
        },
        "sort":{
        "direction":"ascending",
        "timestamp":"last_edited_time"
        }
    }
    try:
        data = json.dumps(queryData)
        response = requests.request("POST", searchUrl, headers=headers, data=data)
        result = response.json()
        logging.info("success", result)
        return result
    except requests.exceptions.RequestException as e:
        logging.error("create fail", str(e))
        return {"result": []}

def createPage(image_url, title, latex, explain):
    createUrl = 'https://api.notion.com/v1/pages'
    children = []
    if image_url:
        children = [{
            "object": "block",
            "type": "file",
            "file": {
                "type": "external",
                "external": {
                "url": image_url
                }
            }
        },{
            "type": "equation",
            "equation": {
                "expression": latex
            }
        },
        ]
    newPageData = {
        "parent": { "database_id": db_id },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
             "LaTex": {
                "rich_text": [
                    {
                        "text": {
                            "content": latex
                        }
                    }
                ]
            },
            "Explain": {
                "rich_text": [
                    {
                        "text": {
                            "content": explain
                        },
                    }
                ]
            },
		},
        "children": children,
    }
    try:
        # response = requests.post(url, headers=headers, json=json)
        data = json.dumps(newPageData)
        response = requests.request("POST", createUrl, headers=headers, data=data)
        result = response.json()
        if response.status_code == 200:
            # print(json.dumps(result, indent=4, sort_keys=True))
            print("create success: ", result)
        else:
            print(response.status_code, result)
    except requests.exceptions.RequestException as e:
        print("create fail", str(e))