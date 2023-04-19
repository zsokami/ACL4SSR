import os
import re
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup

SC_ALIASES_HOSTS = [
    ('dler', 'api.dler.io'),
    ('scs', 'api.subcsub.com'),
]

GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_REF_NAME = os.getenv('GITHUB_REF_NAME')
GITHUB_SHA = os.getenv('GITHUB_SHA')
DDAL_EMAIL = os.getenv('DDAL_EMAIL')
DDAL_PASSWORD = os.getenv('DDAL_PASSWORD')

ini_file_name = next((f for f in os.listdir() if f.endswith('.ini') and 'Full' in f), None)
ini_file_name_nocountry = next((f for f in os.listdir() if f.endswith('.ini') and 'Full' not in f), None)

if DDAL_EMAIL and DDAL_PASSWORD:
    re_ddal_alias = re.compile(r'[\da-z]+(?:-[\da-z]+)*', re.I)

    class DDAL:
        def __init__(self):
            self.__session = requests.Session()
            self.__session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
            self.__token_lock = RLock()

        @staticmethod
        def raise_for_alias(alias):
            if not re_ddal_alias.fullmatch(alias):
                raise Exception(f'非法 alias: {alias}')

        def login(self, email, password):
            with self.__token_lock:
                bs = BeautifulSoup(self.__session.get('https://dd.al/user/login').text, 'html.parser')
                token = bs.find('input', {'name': 'token'})
                if not token:
                    raise Exception('未找到 token (https://dd.al/user/login)')
                token = token['value']
                r = self.__session.post('https://dd.al/user/login', data={
                    'email': email,
                    'password': password,
                    'token': token
                }, allow_redirects=False)
            loc = r.headers.get('Location')
            if not (loc and urlsplit(loc).path == '/user'):
                raise Exception(f'loc = {repr(loc)}')

        def search(self, q) -> list[dict]:
            html = self.__session.post('https://dd.al/user/search', data={
                'q': q,
                'token': 'd2172161243aedc5da47e41227f37add'
            }).text
            bs = BeautifulSoup(html, 'html.parser')
            return [{
                'id': item['data-id'],
                'short': item.select_one('.short-url>a')['href'],
                'original': item.select_one('.title>a')['href']
            } for item in bs.find_all(class_='url-list')]

        def insert(self, alias, url) -> str:
            self.raise_for_alias(alias)
            r = self.__session.post('https://dd.al/shorten', data={
                'url': url,
                'custom': alias
            }).json()
            if r['error']:
                raise Exception(f"{r['msg']} (alias = {repr(alias)}, url = {repr(url)})")
            return r['short']

        def update(self, id, alias, url) -> str:
            for _ in range(10):
                with self.__token_lock:
                    bs = BeautifulSoup(self.__session.get(f'https://dd.al/user/edit/{id}').text, 'html.parser')
                    token = bs.find('input', {'name': 'token'})
                    if not token:
                        raise Exception(f'未找到 token (https://dd.al/user/edit/{id})')
                    token = token['value']
                    r = self.__session.post(f'https://dd.al/user/edit/{id}', data={
                        'url': url,
                        'token': token
                    }, allow_redirects=False)
                loc = r.headers.get('Location')
                if not (loc and urlsplit(loc).path != '/user'):
                    raise Exception(f'loc = {repr(loc)}')
                item = next((item for item in self.search(alias) if item['id'] == id), None)
                if item and item['original'] == url:
                    break
            else:
                raise Exception(f'尝试 10 次更新 url 均失败 (id = {repr(id)}, url = {repr(url)})')
            return item['short']

        def upsert(self, alias, url) -> str:
            self.raise_for_alias(alias)
            id = next((item['id'] for item in self.search(alias) if urlsplit(item['short']).path[1:] == alias), None)
            if id:
                return self.update(id, alias, url)
            else:
                return self.insert(alias, url)

    ddal = DDAL()
    ddal.login(DDAL_EMAIL, DDAL_PASSWORD)

    if GITHUB_REPOSITORY == 'zsokami/ACL4SSR':
        alias, prefix = 'config', ''
    else:
        repo = '-'.join(re_ddal_alias.findall(GITHUB_REPOSITORY))
        alias, prefix = f"gh-{repo}", f"gh-{repo}-"

    def aliases_urls(name, suffix=''):
        if name:
            yield alias + suffix, f"https://ghraw.netlify.app/{GITHUB_REPOSITORY}/{GITHUB_SHA}/{name}"
            _url = f"/sub?target=clash&udp=true&scv=true&config=https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{GITHUB_SHA}/{name}"
            yield from ((prefix + a + suffix, f"https://{h}{_url}") for a, h in SC_ALIASES_HOSTS)

    upsert_args = [
        *aliases_urls(ini_file_name),
        *aliases_urls(ini_file_name_nocountry, '-nc')
    ]

    with ThreadPoolExecutor(len(upsert_args)) as executor:
        for url, *sc_urls in zip(*[executor.map(ddal.upsert, *zip(*upsert_args))]*(1+len(SC_ALIASES_HOSTS))):
            print(url)
            for url in sc_urls:
                print(f"{url}?url=")
else:
    for name in [ini_file_name, ini_file_name_nocountry]:
        if name:
            print(f"https://ghraw.netlify.app/{GITHUB_REPOSITORY}/{GITHUB_REF_NAME}/{name}")
            _url = f"/sub?target=clash&udp=true&scv=true&config=https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{GITHUB_REF_NAME}/{name}?url="
            for _, h in SC_ALIASES_HOSTS:
                print(f"https://{h}{_url}")
