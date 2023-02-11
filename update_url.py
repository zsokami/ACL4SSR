import os

import requests

alias = 'config'
url = f"https://cdn.jsdelivr.net/gh/zsokami/ACL4SSR@{os.getenv('GITHUB_SHA')}/ACL4SSR_Online_Full_Mannix.ini"

session = requests.Session()
session.headers['Authorization'] = 'Bearer wMZJfKSns5lLIZ7if32owHe9w06EVAV6ZjbnCoeFs65PNN95lrwDxnKSGAMV'
api = 'https://goo.gs/api/v1/links'
items = session.get(api, params={'search': alias, 'by': 'alias'}).json()['data']
for item in items:
    if item['alias'] == alias:
        print(session.put(f"{api}/{item['id']}", data={'url': url}).ok)
        break
else:
    print(session.post(api, data={'url': url, 'alias': alias}).ok)
