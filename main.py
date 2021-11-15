import requests, json
import datetime
import argparse
from pocket import pocket_requirements, pocket_fns

parser = argparse.ArgumentParser()
parser.add_argument('--step', type=int, required=True, help='1-3')

########### Pocket ###########
def get_items(consumer_key, access_token):
    get_url = "https://getpocket.com/v3/get"
    action_headers = {
    "Content-Type": "application/json; charset=UTF8",
    "X-Accept": "application/json"
    }
    pocket_params = {
    "consumer_key": consumer_key,
    "access_token": access_token
    }
    pocket_ = requests.request("POST", 
                        url=get_url, 
                        headers=action_headers, 
                        params=pocket_params)
    pocket_data = pocket_.json()
    return pocket_data

def delete_item(consumer_key, access_token, item_id):
    send_url = "https://getpocket.com/v3/send"
    action_headers = {
    "Content-Type": "application/json"
    }
    pocket_params = {
    "consumer_key": consumer_key,
    "access_token": access_token,
    "actions" : [{ 
            "action": "archive",
            "item_id": item_id,
            # "time": ts
        }]
    }
    action = requests.request("POST", 
                    url=send_url, 
                    headers=action_headers, 
                    data=json.dumps(pocket_params))
    # print(action.status_code)
    # print(action.headers.get('X-Error'))
    print("Archived pocket item!")

##############################

########### Notion function###########
def createPage(dbID, headers, title_, url_, ts_):
    pageUrl = "https://api.notion.com/v1/pages"
    pageData = {
        "parent": {"database_id": dbID},
        "properties": {
            "Title": {
                "title": [
                    {"text": {
                        "content": title_
                        }
                    }
                ]
            },
            "URL": {
                "url": url_
            },
            "Time": {
                "date": {
                "start": ts_
                }
            },
            "Read": {
                "checkbox": False
            },
            "Note": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            }
        }
    }
    
    newPage = json.dumps(pageData)
    res = requests.request("POST", pageUrl, headers=headers, data=newPage)
    print("Created new page in Notion!")


def main():
    args = parser.parse_args()

    if args.step == 1:
        with open("./configuration.json") as f:
            data = json.load(f)
        pocket = pocket_requirements(data["pocket"]["consumer_key"], data["pocket"]["redirect_uri"])
        r = pocket.get_RequestToken()
        data["pocket"]["access_non_converted"] = r
        with open("./configuration.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        pocket.get_Credential(r)
    
    if args.step == 2:
        with open("./configuration.json") as f:
            data = json.load(f)
        pocket = pocket_requirements(data["pocket"]["consumer_key"], data["pocket"]["redirect_uri"])
        a = pocket.accessTokenConvertion(data["pocket"]["access_non_converted"])
        data["pocket"]["access_token"] = a
        with open("./configuration.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    if args.step == 3:
        print("Getting pocket item list....")
        with open("./configuration.json") as f:
            data = json.load(f)
        pocket = pocket_fns(data["pocket"]["consumer_key"], data["pocket"]["access_token"])
        pocket_items = pocket.get_items()

        # notion
        notion_token = data["notion"]["token"]
        databaseID = data["notion"]["databaseID"]
        notion_headers = {
            "Authorization": "Bearer " + notion_token,
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json"
        }

        if len(pocket_items["list"]) != 0:
            for key in pocket_items["list"].keys():
                # title
                resolved_title = pocket_items["list"][key]["resolved_title"]
                if resolved_title == "":
                    resolved_title = pocket_items["list"][key]["domain_metadata"]["name"]
                
                # url
                givenUrl = pocket_items["list"][key]["given_url"]
                
                # added time
                timestamp = pocket_items["list"][key]["time_added"]
                ts = datetime.datetime.fromtimestamp(int(timestamp))
                ts_ = f"{ts:%Y-%m-%dT%H:%M:%S}"

                createPage(databaseID, notion_headers, resolved_title, givenUrl, ts_)

                pocket.delete_item("archive", key)
        else:
            print("No item in pocket! :(")


if __name__ == "__main__":
    main()