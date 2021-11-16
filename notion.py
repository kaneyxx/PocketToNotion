import requests, json

########### Notion function###########
# For custom page, please visit: https://developers.notion.com/reference/page#property-value-object for details

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
