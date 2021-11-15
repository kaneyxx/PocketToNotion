# Pocket to Notion

Prepare your configuration.json file as below:
```json
{
    "pocket": {
        "consumer_key": "",
        "redirect_uri": ""
    },
    "notion": {
        "token": "",
        "databaseID": ""
    }
}
```
- Pocket
> 1. Go to https://getpocket.com/developer/apps/new create your app (Remember checking all permissions!)
> 2. Get the consumer key, and decide your redirect_uri 

- Notion
> 1. Go to https://www.notion.so/my-integrations and get your Internal Integration Token
> 2. copy Notion database link to browser and get the ID, e.g. https://www.notion.so/workspace/[DATABASEID]?v=12345678 , the database ID is 32 characters

Command:
```python
python main.py [--step 1-3]
```
step 1: Being authorized  
step 2: Get the access token  
step 3: Archived pocket items and dump into Notion