import os

import requests

API_KEY = os.getenv('API_KEY')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

if GITHUB_REPOSITORY == 'zsokami/ACL4SSR':
    alias = 'config'
    alias_sc = 'dler'
else:
    repo = GITHUB_REPOSITORY.replace('/', '__')
    alias = f"gh__{repo}"
    alias_sc = f"gh__{repo}__sc"

ini_file_name = next(f for f in os.listdir() if f.endswith('.ini'))
url = f"https://cdn.jsdelivr.net/gh/{GITHUB_REPOSITORY}@{os.getenv('GITHUB_SHA')}/{ini_file_name}"
url_sc = f"https://api.dler.io/sub?target=clash&udp=true&scv=true&config={url}"

session = requests.Session()
session.headers['Authorization'] = f"Bearer {API_KEY}"
api = 'https://goo.gs/api/v1/links'


def upsert(alias, url):
    items = session.get(api, params={'search': alias, 'by': 'alias'}).json()['data']
    item = next((item for item in items if item['alias'] == alias), None)
    if item:
        print(session.put(f"{api}/{item['id']}", data={'url': url}).ok)
    else:
        print(session.post(api, data={'url': url, 'alias': alias}).ok)


upsert(alias, url)
upsert(alias_sc, url_sc)
