import requests, json
import webbrowser

class pocket_requirements():
    def __init__(self, consumer_key, redirect_url=None):
        self.consumer_key = consumer_key
        self.redirect_url = redirect_url
    
    def get_RequestToken(self):
        request_url = "https://getpocket.com/v3/oauth/request"
        params = {
            "consumer_key": self.consumer_key,
            "redirect_uri": self.redirect_url
        }
        headers = {
            "Content-Type": "application/json; charset=UTF8",
            "X-Accept": "application/json"
        }
        res = requests.request("POST", 
                              url=request_url, 
                              headers=headers, 
                              params=params)
        data = res.json()
        requestToken = data["code"]
        
        return requestToken
    
    def get_Credential(self, requestToken):
        oauth_url = "https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}".format(requestToken, self.redirect_url)
        webbrowser.open(oauth_url)
    
    def accessTokenConvertion(self, requestToken):
        params = {
            "consumer_key": self.consumer_key,
            "code": requestToken
        }
        headers = {
            "Content-Type": "application/json; charset=UTF8",
            "X-Accept": "application/json"
        }
        res = requests.request("POST", 
                            url="https://getpocket.com/v3/oauth/authorize", 
                            headers=headers,
                            params=params)
        data = res.json()
        accessToken = data["access_token"]
        # userName = data["username"]
        print("access token: ", accessToken)

        return accessToken

class pocket_fns():
    def __init__(self, consumer_key, access_token):
        self.consumer_key = consumer_key
        self.access_token = access_token
    
    def get_items(self):
        get_url = "https://getpocket.com/v3/get"
        action_headers = {
        "Content-Type": "application/json; charset=UTF8",
        "X-Accept": "application/json"
        }
        pocket_params = {
        "consumer_key": self.consumer_key,
        "access_token": self.access_token
        }
        pocket_ = requests.request("POST", 
                            url=get_url, 
                            headers=action_headers, 
                            params=pocket_params)
        pocket_data = pocket_.json()
        return pocket_data
    
    def delete_item(self, action, item_id):
        send_url = "https://getpocket.com/v3/send"
        action_headers = {
        "Content-Type": "application/json"
        }
        pocket_params = {
        "consumer_key": self.consumer_key,
        "access_token": self.access_token,
        "actions" : [{ 
                "action": action,
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