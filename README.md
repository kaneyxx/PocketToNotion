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
> 2. Get the consumer key, and decide your redirect_uri (e.g. http://www.google.com)

- Notion
> 1. Go to https://www.notion.so/my-integrations and get your Internal Integration Token
> 2. Click the share button on database, then invite the integration you just created
> 3. copy Notion database link to browser and get the ID, e.g. https://www.notion.so/workspace/[DATABASEID]?v=12345678 , the database ID is 32 characters

* Notion table columns (notion data type):  
  "Title" (title)  
  "URL" (url)  
  "Time" (ISO8601 time format)  
  "Read" (checkbox)  
  "Note" (rich text)  
**Feel free to modify as your table design :)**

Command:
```python
python main.py [--step 1-3]
```
step 1: Being authorized  
step 2: Get the access token
(step1 & 2 only need to run once)  
step 3: Archived pocket items and dump into Notion