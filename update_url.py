import os
import re
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from time import sleep
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry

SC_ALIASES_HOSTS = [
    ('scm', 'scm.onrender.com'),
    ('dler', 'api.dler.io'),
    ('scs', 'api.subcsub.com'),
]

GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_REF_NAME = os.getenv('GITHUB_REF_NAME')
GITHUB_SHA = os.getenv('GITHUB_SHA')
API_KEY = os.getenv('URL_SHORTENER_API_KEY')

GITHUB_REPOSITORY_RAW_URL_PREFIX = f'https://ghraw.onrender.com/{GITHUB_REPOSITORY}/'

ini_file_name = next((f for f in os.listdir() if f.endswith('.ini') and 'Full' in f), None)
ini_file_name_nocountry = next((f for f in os.listdir() if f.endswith('.ini') and 'Full' not in f), None)


if API_KEY:
    re_scheme = re.compile(r'^(?:(https?):)?[\\/]*', re.I)

    class URLShortener:
        def __init__(self, base=None):
            self.__session = requests.Session()
            self.__session.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.1)))
            self.__session.mount('http://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.1)))
            self.__session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
            self._token_lock = RLock()
            self.set_base(base)

        @property
        def session(self):
            return self.__session

        def set_base(self, base):
            if base:
                self.__base = re_scheme.sub(lambda m: f"{m[1] or 'https'}://", base.split('#', 1)[0])
            else:
                self.__base = ''

        @property
        def base(self):
            return self.__base

        def get(self, url='', timeout=10, **kwargs):
            return self.__session.get(urljoin(self.base, url), timeout=timeout, **kwargs)

        def post(self, url='', *args, timeout=10, **kwargs):
            return self.__session.post(urljoin(self.base, url), *args, timeout=timeout, **kwargs)

        def put(self, url='', *args, timeout=10, **kwargs):
            return self.__session.put(urljoin(self.base, url), *args, timeout=timeout, **kwargs)

        def submit(self, page_url='', form_id=None, form_action=None, headers=None, **kwargs):
            with self._token_lock:
                r = self.get(page_url)
                if not r.ok:
                    return None
                doc = BeautifulSoup(r.text, 'html.parser')
                form = doc.find(
                    'form',
                    **({} if form_id is None else {'id': form_id}),
                    **({} if form_action is None else {'action': form_action}),
                )
                data = {}
                for tag in form.find_all(attrs={'name': True}):
                    if tag['name'] not in data or tag.has_attr('checked'):
                        selected = tag.find(selected=True)
                        data[tag['name']] = selected['value'] if selected else tag.get('value', '')
                data.update(kwargs)
                return self.post(form['action'], headers=headers, data=data, allow_redirects=False)

        def upsert(self, alias, url) -> str: ...

    class URLShortenerA(URLShortener):
        re_alias = re.compile(r'^[\da-z]+(?:-[\da-z]+)*$', re.I)
        re_item_tag_id = re.compile(r'^link-(\d+)$')

        def __init__(self, host, email, password=None):
            super().__init__(host)
            self.login(email, password or email)

        @staticmethod
        def bs(text):
            doc = BeautifulSoup(text, 'html.parser')
            if alert := doc.find(class_='alert'):
                raise Exception(alert.text)
            return doc

        @classmethod
        def raise_for_alias(cls, alias):
            if not cls.re_alias.fullmatch(alias):
                raise Exception(f'非法 alias: {alias}')

        def login(self, email, password):
            loc = None
            for i in range(20):
                with self._token_lock:
                    doc = self.bs(self.get('user/login').text)
                    if i > 0:
                        sleep(9)
                    token = doc.find('input', {'name': 'token'})
                    if token:
                        token = token['value']
                        r = self.post('user/login', data={
                            'email': email,
                            'password': password,
                            'token': token
                        }, allow_redirects=False)
                        loc = r.headers.get('Location')
                if loc and urlsplit(loc).path == '/user':
                    break
            else:
                raise Exception(f'尝试 20 次登录均失败 (loc = {loc!r})')

        def search(self, q) -> list[dict]:
            doc = self.bs(self.post('user/search', data={
                'q': q,
            }).text)
            return [{
                'id': item['data-id'],
                'short': item.select_one('.short-url>a')['href'],
                'original': item.select_one('.title>a')['href']
            } for item in doc.find_all(class_='url-list')]

        def insert(self, alias, url) -> str:
            self.raise_for_alias(alias)
            r = self.post('shorten', data={
                'url': url,
                'custom': alias
            }).json()
            if r['error']:
                raise Exception(f"{r['msg']} (alias = {alias!r}, url = {url!r})")
            return r['short']

        def update(self, id, alias, url) -> str:
            self.raise_for_alias(alias)
            for _ in range(10):
                with self._token_lock:
                    doc = self.bs(self.get(f'user/edit/{id}').text)
                    token = doc.find('input', {'name': 'token'})
                    if not token:
                        raise Exception(f'未找到 token (user/edit/{id})')
                    token = token['value']
                    r = self.post(f'user/edit/{id}', data={
                        'url': url,
                        'token': token
                    }, allow_redirects=False)
                loc = r.headers.get('Location')
                if not (loc and urlsplit(loc).path != '/user'):
                    raise Exception(f'loc = {loc!r}')
                item = next((item for item in self.search(alias) if item['id'] == id), None)
                if item and item['original'] == url:
                    break
            else:
                raise Exception(f'尝试 10 次更新 url 均失败 (id = {id!r}, url = {url!r})')
            return item['short']

        def upsert(self, alias, url) -> str:
            self.raise_for_alias(alias)
            id = next((item['id'] for item in self.search(alias) if urlsplit(item['short']).path[1:] == alias), None)
            if id:
                return self.update(id, alias, url)
            else:
                return self.insert(alias, url)

    class URLShortenerA2(URLShortenerA):
        def login(self, email, password):
            loc = None
            for i in range(20):
                with self._token_lock:
                    doc = self.bs(self.get('user/login').text)
                    if i > 0:
                        sleep(9)
                    token = doc.find('input', {'name': '_token'})
                    if token:
                        token = token['value']
                        r = self.post('user/login/auth', data={
                            'email': email,
                            'password': password,
                            '_token': token
                        }, allow_redirects=False)
                        loc = r.headers.get('Location')
                if loc and urlsplit(loc).path == '/user':
                    break
            else:
                raise Exception(f'尝试 20 次登录均失败 (loc = {loc!r})')

        def search(self, q) -> list[dict]:
            doc = self.bs(self.get('user/search', params={
                'q': q,
            }).text)
            return [{
                'id': self.re_item_tag_id.match(item['id'])[1],
                'short': item.find(attrs={'data-href': True})['data-href'],
                'original': item.find(rel='nofollow')['href']
            } for item in doc.find_all(id=self.re_item_tag_id)]

        def insert(self, alias, url) -> str:
            self.raise_for_alias(alias)
            r = self.post('shorten', data={
                'url': url,
                'custom': alias
            }).json()
            if r['error']:
                raise Exception(f"{r['message']} (alias = {alias!r}, url = {url!r})")
            return r['data']['shorturl']

        def update(self, id, alias, url) -> str:
            self.raise_for_alias(alias)
            for _ in range(10):
                with self._token_lock:
                    doc = self.bs(self.get(f'user/links/{id}/edit').text)
                    token = doc.find('input', {'name': '_token'})
                    if not token:
                        raise Exception(f'未找到 token (user/edit/{id})')
                    token = token['value']
                    r = self.post(f'user/links/{id}/update', data={
                        'url': url,
                        '_token': token
                    }, allow_redirects=False)
                loc = r.headers.get('Location')
                if not (loc and urlsplit(loc).path != '/user'):
                    raise Exception(f'loc = {loc!r}')
                item = next((item for item in self.search(alias) if item['id'] == id), None)
                if item and item['original'] == url:
                    break
            else:
                raise Exception(f'尝试 10 次更新 url 均失败 (id = {id!r}, url = {url!r})')
            return item['short']

    class URLShortenerB(URLShortener):
        def __init__(self, host, api_key, domain_id=None):
            super().__init__(f'{host}/api/v1/links/')
            self.session.headers['Authorization'] = f'Bearer {api_key}'
            self.param_name_search_by = 'search_by'
            self.param_name_domain_id = 'domain_id'
            if domain_id is None:
                doc = self.get('/developers/links').text
                if '<code>by</code>' in doc:
                    self.param_name_search_by = 'by'
                    self.param_name_domain_id = None
                    domain_id = 0
                else:
                    if '<code>domain</code>' in doc:
                        self.param_name_domain_id = 'domain'
                    domain_id = 1
            elif not domain_id:
                self.param_name_search_by = 'by'
                self.param_name_domain_id = None
            self.domain_id = domain_id

        def upsert(self, alias, url) -> str:
            resp = self.get(params={'search': alias, self.param_name_search_by: 'alias'})
            items = resp.json()['data']
            item = next((item for item in items if item['alias'] == alias), None)
            if item:
                r = self.put(str(item['id']), data={'url': url})
            else:
                endpoint = ''
                for _ in range(5):
                    r = self.post(endpoint, data={
                        'url': url,
                        'alias': alias,
                        **({self.param_name_domain_id: self.domain_id} if self.domain_id else {})
                    }, allow_redirects=False)
                    if not r.is_redirect:
                        break
                    endpoint = r.headers['Location']
            if 200 <= r.status_code < 300:
                return r.json()['data']['short_url']
            raise Exception(r.status_code, r.text)

    class URLShortener5XTO(URLShortener):
        def __init__(self, host, api_key):
            super().__init__(f'{host}/api/links/')
            self.session.headers['Authorization'] = f'Bearer {api_key}'

        def upsert(self, alias, url) -> str:
            item = next((item for item in self.get(params={
                'results_per_page': 500
            }).json()['data'] if item['url'] == alias), None)
            if item:
                r = self.post(str(item['id']), data={'location_url': url})
            else:
                r = self.post(data={'location_url': url, 'url': alias})
            if 200 <= r.status_code < 300:
                return urljoin(self.base, f'/{alias}')
            raise Exception(r.status_code, r.text)

    class URLShortenerGGGG(URLShortener):
        def __init__(self, host, email, password=None):
            super().__init__(host)
            self.login(email, password or email.split('@')[0])

        def login(self, email, password):
            r = self.post('auth/login', data={'identity': email, 'password': password}, allow_redirects=False)
            if r.status_code != 200:
                raise Exception(r.status_code, r.text)

        def upsert(self, alias, url) -> str:
            item = next((item for item in self.post('search', {'query': ''}).json() if item['link'] == alias), None)
            if item:
                r = self.post('update', data={'custom_path': alias, 'long_url': url, 'link_id': item['id']})
                if r.status_code == 200 and r.text != 'Error!':
                    return urljoin(self.base, f'/{r.text}')
            else:
                r = self.post('create', data={'custom_path': alias, 'long_url': url})
                u = urlsplit(r.text)
                if r.status_code == 200 and u.hostname == urlsplit(self.base).hostname and u.path != '/':
                    return urljoin(self.base, u.path)
            raise Exception(r.status_code, r.text)

    class URLShortenerAdLinkFly(URLShortener):
        def __init__(self, host, username, password=None):
            super().__init__(host)
            self.login(username, password or username.split('@')[0])

        def login(self, username, password):
            if not (r := self.submit('auth/signin', 'signin-form', username=username, password=password)):
                raise Exception()
            if not ((loc := r.headers.get('Location')) and urlsplit(loc).path == '/member/dashboard'):
                raise Exception(r.status_code, r.text)

        def upsert(self, alias, url) -> str:
            if r := self.submit(f'member/links/edit/{alias}', False, url=url):
                if (loc := r.headers.get('Location')) and urlsplit(loc).path == urlsplit(r.url).path:
                    return urljoin(self.base, alias)
                raise Exception(r.status_code, r.text)
            if r := self.submit(f'member/links?alias={alias}', 'shorten', headers={'X-Requested-With': 'XMLHttpRequest'}, url=url, alias=alias, ad_type=0):
                if r.json().get('url'):
                    return urljoin(self.base, alias)
                raise Exception(r.status_code, r.text)
            raise Exception()

    class URLShortenerPolr(URLShortener):
        def __init__(self, host, username, password=None):
            super().__init__(host)
            self.login(username, password or username)

        def login(self, username, password):
            if not (r := self.submit(form_action='login', username=username, password=password)):
                raise Exception()
            if not ((loc := r.headers.get('Location')) and urlsplit(loc).path == ''):
                raise Exception(r.status_code, r.text)

        def upsert(self, alias, url) -> str:
            with self._token_lock:
                doc = BeautifulSoup(self.get('admin').text, 'html.parser')
                if not (tag := doc.find('meta', attrs={'name': 'csrf-token'})):
                    raise Exception('未找到 csrf-token')
                r = self.post(
                    'api/v2/admin/edit_link_long_url',
                    headers={'X-Csrf-Token': tag['content']},
                    data={'link_ending': alias, 'new_long_url': url}
                )
            if r.status_code == 200:
                return urljoin(self.base, alias)
            if tag_api_key := doc.select_one('#developer input'):
                r = self.get('api/v2/action/shorten', params={
                    'key': tag_api_key['value'],
                    'url': url,
                    'custom_ending': alias,
                })
                if r.status_code == 200:
                    return urljoin(self.base, alias)
            else:
                if not (r := self.submit(form_action='/shorten', **{'link-url': url, 'custom-ending': alias})):
                    raise Exception()
                if r.status_code == 200:
                    return urljoin(self.base, alias)
            raise Exception(r.status_code, r.text)

    def guess_url_shortener(host):
        session = requests.Session()
        base = f'https://{host}/'
        doc = session.get(base).text
        if 'ng-app="polr"' in doc:
            return URLShortenerPolr
        doc = BeautifulSoup(session.get(f'{base}user/login').text, 'html.parser')
        if doc.find('input', {'name': 'token'}):
            return URLShortenerA
        if doc.find('input', {'name': '_token'}):
            return URLShortenerA2
        doc = BeautifulSoup(session.get(f'{base}login').text, 'html.parser')
        if doc.find('input', {'name': '_token'}):
            return URLShortenerB
        r = session.get(f'{base}api/links')
        if r.status_code == 401 and 'json' in r.headers.get('Content-Type', ''):
            return URLShortener5XTO
        r = session.get(f'{base}js/logic.js')
        if r.status_code == 200 and "'/create'" in r.text:
            return URLShortenerGGGG
        r = session.get(f'{base}auth/signin')
        if r.status_code == 200 and '"/auth/signin"' in r.text:
            return URLShortenerAdLinkFly
        return None

    url_shortener = URLShortenerB('u.fail', API_KEY, 1)

    if GITHUB_REPOSITORY == 'zsokami/ACL4SSR':
        alias, prefix = 'config', ''
    else:
        repo = '-'.join(URLShortenerA.re_alias.findall(GITHUB_REPOSITORY))
        alias, prefix = f"gh-{repo}", f"gh-{repo}-"

    def aliases_urls(name, suffix=''):
        if name:
            yield alias + suffix, f"{GITHUB_REPOSITORY_RAW_URL_PREFIX}{GITHUB_SHA}/{name}"
            _url = f"/sub?target=clash&udp=true&scv=true&config=https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{GITHUB_SHA}/{name}"
            yield from ((prefix + a + suffix, f"https://{h}{_url}") for a, h in SC_ALIASES_HOSTS)

    upsert_args = [
        *aliases_urls(ini_file_name),
        *aliases_urls(ini_file_name_nocountry, '-nc')
    ]

    with ThreadPoolExecutor(len(upsert_args)) as executor:
        for url, *sc_urls in zip(*[executor.map(url_shortener.upsert, *zip(*upsert_args))]*(1+len(SC_ALIASES_HOSTS))):
            print(url)
            for url in sc_urls:
                print(f"{url}?url=")
else:
    for name in [ini_file_name, ini_file_name_nocountry]:
        if name:
            print(f"{GITHUB_REPOSITORY_RAW_URL_PREFIX}{GITHUB_REF_NAME}/{name}")
            _url = f"/sub?target=clash&udp=true&scv=true&config=https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{GITHUB_REF_NAME}/{name}?url="
            for _, h in SC_ALIASES_HOSTS:
                print(f"https://{h}{_url}")
