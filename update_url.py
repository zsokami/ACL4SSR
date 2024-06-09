import os
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import RLock
from time import sleep
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry

SC_ALIASES_HOSTS = [
    ('v1', 'url.v1.mk'),
    ('dler', 'api.dler.io'),
    ('id9', 'sub.id9.cc'),
    ('0z', 'api-suc.0z.gs'),
]

GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_REF_NAME = os.getenv('GITHUB_REF_NAME')
GITHUB_SHA = os.getenv('GITHUB_SHA')
URL_SHORTENER_API_KEY = os.getenv('URL_SHORTENER_API_KEY')
URL_SHORTENER_TYPE, URL_SHORTENER_HOST = 'Shortio', 'api.short.io'
URL_SHORTENER_OPTIONS = {'host': URL_SHORTENER_HOST, 'api_key': URL_SHORTENER_API_KEY, 'domain': 'mnnx.cc'}

GITHUB_REPOSITORY_RAW_URL_PREFIX = f'https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/'

ini_file_name = next((f for f in os.listdir() if f.endswith('.ini') and 'Full' in f), None)
ini_file_name_nocountry = next((f for f in os.listdir() if f.endswith('.ini') and 'Full' not in f), None)


if URL_SHORTENER_API_KEY:
    re_scheme = re.compile(r'^(?:(https?):)?[\\/]*', re.I)

    def bs(text):
        return BeautifulSoup(text, 'html.parser')

    def to_base(part):
        return re_scheme.sub(lambda m: f"{m[1] or 'https'}://", part.split('#', 1)[0]) if part else ''

    def to_https(url):
        return re_scheme.sub('https://', url)

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
            self.__base = to_base(base)

        @property
        def base(self):
            return self.__base

        def get(self, url='', timeout=10, **kwargs):
            return self.__session.get(urljoin(self.base, url), timeout=timeout, **kwargs)

        def post(self, url='', *args, timeout=10, **kwargs):
            return self.__session.post(urljoin(self.base, url), *args, timeout=timeout, **kwargs)

        def put(self, url='', *args, timeout=10, **kwargs):
            return self.__session.put(urljoin(self.base, url), *args, timeout=timeout, **kwargs)

        def patch(self, url='', *args, timeout=10, **kwargs):
            return self.__session.patch(urljoin(self.base, url), *args, timeout=timeout, **kwargs)

        def submit(
            self,
            page_url_or_bs: str | BeautifulSoup = '',
            form_id=None,
            form_name=None,
            form_action=None,
            headers=None,
            post_url=None,
            **kwargs
        ):
            with self._token_lock:
                if isinstance(page_url_or_bs, str):
                    r = self.get(page_url_or_bs)
                    if not r.ok:
                        return None
                    doc = bs(r.text)
                else:
                    doc = page_url_or_bs
                form = doc.find(
                    'form',
                    attrs={k: v for k, v in [
                        ('id', form_id),
                        ('name', form_name),
                        ('action', form_action),
                    ] if v is not None}
                )
                if not form:
                    return None
                data = {}
                for tag in form.find_all(attrs={'name': True}):
                    if tag['name'] and (tag['name'] not in data or tag.has_attr('checked')):
                        if tag.get('type') == 'checkbox':
                            if tag.has_attr('checked'):
                                data[tag['name']] = tag.get('value', 'on')
                        elif tag.name == 'select':
                            if selected := tag.find('option', selected=True) or tag.find('option'):
                                data[tag['name']] = selected.get('value', selected.text)
                        else:
                            data[tag['name']] = tag.get('value', '')
                data.update(kwargs)
                return self.post(post_url or form['action'], headers=headers, data=data, allow_redirects=False)

        @classmethod
        def check(cls, host):
            try:
                return bool(cls._check(partial(URLShortener(host).get, timeout=5, allow_redirects=False)))
            except Exception:
                return False

        def upsert(self, alias, url) -> str: ...

        @staticmethod
        def _check(get): ...

    class URLShortenerA(URLShortener):
        re_alias = re.compile(r'[\da-z]+(?:-[\da-z]+)*', re.I)
        re_item_tag_id = re.compile(r'^link-(\d+)$')

        def __init__(self, host, email=None, password=None, domain=None):
            super().__init__(host)
            if email:
                self.login(email, password or email)
            self.domain = to_base(domain)

        @staticmethod
        def bs(text):
            doc = bs(text)
            if (alert := doc.find(class_='alert')) and '已成功' not in alert.text:
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
                'token': '19ea4506a3aaee52e4c8b98c3a59a3d2'
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
                'custom': alias,
                **({'domain': self.domain} if self.domain else {})
            }).json()
            if r['error']:
                raise Exception(f"{r['msg']} (alias = {alias!r}, url = {url!r})")
            return to_https(r['short'])

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
                        'token': token,
                        **({'domain': self.domain} if self.domain else {})
                    }, allow_redirects=False)
                loc = r.headers.get('Location')
                if not (loc and urlsplit(loc).path != '/user'):
                    raise Exception(f'loc = {loc!r}')
                item = next((item for item in self.search(alias) if item['id'] == id), None)
                if item and item['original'] == url:
                    break
            else:
                raise Exception(f'尝试 10 次更新 url 均失败 (id = {id!r}, url = {url!r})')
            return to_https(item['short'])

        def upsert(self, alias, url) -> str:
            self.raise_for_alias(alias)
            id = next((item['id'] for item in self.search(alias) if urlsplit(item['short']).path[1:] == alias), None)
            if id:
                return self.update(id, alias, url)
            else:
                return self.insert(alias, url)

        @staticmethod
        def _check(get):
            return bs(get('user/login').text).find('input', {'name': 'token'})

    class URLShortenerA2(URLShortenerA):
        def __init__(self, host, email=None, password=None, domain=None, api_key=None):
            super().__init__(host, email, password, domain)
            if api_key:
                self.session.headers['Authorization'] = f'Bearer {api_key}'

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
                'custom': alias,
                **({'domain': self.domain} if self.domain else {})
            }).json()
            if r['error']:
                raise Exception(f"{r['message']} (alias = {alias!r}, url = {url!r})")
            return to_https(r['data']['shorturl'])

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
                        '_token': token,
                        **({'domain': self.domain} if self.domain else {})
                    }, allow_redirects=False)
                loc = r.headers.get('Location')
                if not (loc and urlsplit(loc).path != '/user'):
                    raise Exception(f'loc = {loc!r}')
                item = next((item for item in self.search(alias) if item['id'] == id), None)
                if item and item['original'] == url:
                    break
            else:
                raise Exception(f'尝试 10 次更新 url 均失败 (id = {id!r}, url = {url!r})')
            return to_https(item['short'])

        def upsert(self, alias, url) -> str:
            if 'Authorization' not in self.session.headers:
                return super().upsert(alias, url)
            r = self.get('api/urls?limit=500')
            if not r.ok or r.json()['error']:
                raise Exception(r.status_code, r.text)
            if item := next((item for item in r.json()['data']['urls'] if item['alias'] == alias), None):
                r = self.put(f"api/url/{item['id']}/update", json={
                    'url': url,
                    **({'domain': self.domain} if self.domain else {})
                })
            else:
                r = self.post('api/url/add', json={
                    'url': url,
                    'custom': alias,
                    'type': 'direct',
                    **({'domain': self.domain} if self.domain else {})
                })
            if not r.ok or r.json()['error']:
                raise Exception(r.status_code, r.text)
            return to_https(r.json()['shorturl'])

        @staticmethod
        def _check(get):
            return (r := get('user/login')) and bs(r.text).find('input', {'name': '_token'})

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
            r = self.get(params={'search': alias, self.param_name_search_by: 'alias'})
            if not r.ok:
                raise Exception(r.status_code, r.text)
            items = r.json()['data']
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
                return to_https(r.json()['data']['short_url'])
            raise Exception(r.status_code, r.text)

        @staticmethod
        def _check(get):
            return 'https://rsms.me' in (t := get('login').text) and bs(t).find('input', {'name': '_token'})

    class URLShortener5XTO(URLShortener):
        def __init__(self, host, email=None, password=None, api_key=None, domain_id=None, domain=None):
            if api_key:
                super().__init__(f'{host}/api/links/')
                self.session.headers['Authorization'] = f'Bearer {api_key}'
            else:
                super().__init__(host)
                self.login(email, password or email)
            self.domain_id = domain_id
            self.domain = to_base(domain)

        def login(self, email, password):
            r = self.post('login', data={'email': email, 'password': password}, allow_redirects=False)
            if not ((loc := r.headers.get('Location')) and urlsplit(loc).path == '/dashboard'):
                raise Exception(r.status_code, r.text)

            with self._token_lock:
                doc = bs(self.get(loc).text)
                if tag := doc.find('div', attrs={'data-project-id': True}):
                    self.project_url = tag.find('a')['href']
                else:
                    if (r := self.submit(doc, form_name='create_project', post_url='project-ajax', name=email)) is None:
                        self.project_url = 'links?type=link'
                    elif r.status_code == 200 and r.json().get('status') == 'success':
                        self.project_url = r.json()['details']['url']
                    else:
                        raise Exception(r.status_code, r.text)

        def upsert_api(self, alias, url) -> str:
            r = self.get(params={
                'results_per_page': 500
            })
            if not r.ok:
                raise Exception(r.status_code, r.text)
            item = next((item for item in r.json()['data'] if item['url'] == alias), None)
            if item:
                r = self.post(str(item['id']), data={'location_url': url, 'url': alias})
            else:
                r = self.post(data={
                    'location_url': url,
                    'url': alias,
                    **({} if self.domain_id is None else {'domain_id': self.domain_id})
                })
            if 200 <= r.status_code < 300:
                return to_https(urljoin(self.domain or self.base, f'/{alias}'))
            raise Exception(r.status_code, r.text)

        def upsert(self, alias, url) -> str:
            if 'Authorization' in self.session.headers:
                return self.upsert_api(alias, url)
            with self._token_lock:
                doc = bs(self.get(self.project_url).text)
                if tag := next((tag for tag in [tag.find('a') for tag in doc.find_all('div', class_='custom-row')] if tag.text == alias), None):
                    r = self.submit(tag['href'], form_name='update_link', post_url='link-ajax', location_url=url)
                else:
                    r = self.submit(
                        doc,
                        form_name='create_link',
                        post_url='link-ajax',
                        url=alias,
                        location_url=url,
                        **({} if self.domain_id is None else {'domain_id': self.domain_id})
                    )
            if r is None:
                raise Exception()
            if r.status_code != 200 or r.json().get('status') != 'success':
                raise Exception(r.status_code, r.text)
            return to_https(urljoin(self.domain or self.base, alias))

        @staticmethod
        def _check(get):
            doc = bs(get('login').text)
            return doc.find('input', {'name': 'email', 'class': 'form-control'}) and not doc.find('input', {'name': '_token'})

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
                    return to_https(urljoin(self.base, f'/{r.text}'))
            else:
                r = self.post('create', data={'custom_path': alias, 'long_url': url})
                u = urlsplit(r.text)
                if r.status_code == 200 and u.hostname == urlsplit(self.base).hostname and u.path != '/':
                    return to_https(urljoin(self.base, u.path))
            raise Exception(r.status_code, r.text)

        @staticmethod
        def _check(get):
            return "'/create'" in get('js/logic.js').text

    class URLShortenerAdLinkFly(URLShortener):
        def __init__(self, host, username, password=None, **kwargs):
            super().__init__(host)
            self.login(username, password or username.split('@')[0])
            self.kwargs = kwargs or {'ad_type': 0}
            self.domain = to_base(kwargs.get('domain'))

        def login(self, username, password):
            if (r := self.submit('auth/signin', 'signin-form', username=username, password=password)) is None:
                raise Exception()
            if not ((loc := r.headers.get('Location')) and urlsplit(loc).path == '/member/dashboard'):
                raise Exception(r.status_code, r.text)

        def upsert(self, alias, url) -> str:
            if (r := self.submit(f'member/links/edit/{alias}', False, url=url)) is not None:
                if (loc := r.headers.get('Location')) and urlsplit(loc).path == urlsplit(r.url).path:
                    return to_https(urljoin(self.domain or self.base, alias))
                raise Exception(r.status_code, r.text)
            if (r := self.submit(f'member/links?alias={alias}', 'shorten', headers={'X-Requested-With': 'XMLHttpRequest'}, url=url, alias=alias, **self.kwargs)) is not None:
                if r.json().get('url'):
                    return to_https(urljoin(self.domain or self.base, alias))
                raise Exception(r.status_code, r.text)
            raise Exception()

        @staticmethod
        def _check(get):
            return '"/auth/signin"' in get('auth/signin').text

    class URLShortenerPolr(URLShortener):
        def __init__(self, host, username, password=None):
            super().__init__(host)
            self.login(username, password or username)

        def login(self, username, password):
            if (r := self.submit(form_action='login', username=username, password=password)) is None:
                raise Exception()
            if not ((loc := r.headers.get('Location')) and urlsplit(loc).path == ''):
                raise Exception(r.status_code, r.text)

        def upsert(self, alias, url) -> str:
            with self._token_lock:
                doc = bs(self.get('admin').text)
                if not (tag := doc.find('meta', attrs={'name': 'csrf-token'})):
                    raise Exception('未找到 csrf-token')
                r = self.post(
                    'api/v2/admin/edit_link_long_url',
                    headers={'X-Csrf-Token': tag['content']},
                    data={'link_ending': alias, 'new_long_url': url}
                )
            if r.status_code == 200:
                return to_https(urljoin(self.base, alias))
            if tag_api_key := doc.select_one('#developer input'):
                r = self.get('api/v2/action/shorten', params={
                    'key': tag_api_key['value'],
                    'url': url,
                    'custom_ending': alias,
                })
                if r.status_code == 200:
                    return to_https(urljoin(self.base, alias))
            else:
                if (r := self.submit(form_action='/shorten', **{'link-url': url, 'custom-ending': alias})) is None:
                    raise Exception()
                if r.status_code == 200:
                    return to_https(urljoin(self.base, alias))
            raise Exception(r.status_code, r.text)

        @staticmethod
        def _check(get):
            return 'ng-app="polr"' in get().text

    class URLShortenerKutt(URLShortener):
        def __init__(self, host, api_key, domain=None):
            super().__init__(f'{host}/api/v2/links/')
            self.session.headers['X-API-KEY'] = api_key
            self.domain = to_base(domain)

        def upsert(self, alias, url) -> str:
            r = self.get(params={
                'limit': 500,
                'search': alias,
            })
            if not r.ok:
                raise Exception(r.status_code, r.text)
            item = next((item for item in r.json()['data'] if item['address'] == alias), None)
            if item:
                r = self.patch(str(item['id']), data={'target': url, 'address': alias})
            else:
                r = self.post(data={'target': url, 'customurl': alias})
            if 200 <= r.status_code < 300:
                return to_https(urljoin(self.domain, alias) if self.domain else r.json()['link'])
            raise Exception(r.status_code, r.text)

        @staticmethod
        def _check(get):
            return get('api/v2/health').text == 'OK'

    class URLShortenerShortio(URLShortener):
        def __init__(self, host, api_key, domain):
            super().__init__(f'{host}/links/')
            self.session.headers['Authorization'] = api_key
            self.domain = domain

        def upsert(self, alias, url) -> str:
            r = self.get('expand', params={'domain': self.domain, 'path': alias})
            if r.status_code == 200:
                r = self.post(r.json()['idString'], json={'originalURL': url})
            elif r.status_code == 404:
                r = self.post(json={'domain': self.domain, 'originalURL': url, 'path': alias})
            else:
                raise Exception(r.status_code, r.text)
            if r:
                return r.json()['shortURL']
            raise Exception(r.status_code, r.text)

        @staticmethod
        def _check(get):
            return get().text == '{"success":true}'

    def guess_url_shortener_type(host):
        get = partial(URLShortener(host).get, timeout=5, allow_redirects=False)
        doc = get().text
        if 'ng-app="polr"' in doc:
            return 'Polr'
        if doc == '{"success":true}':
            return 'Shortio'
        doc = bs(get('user/login').text)
        if doc.find('input', {'name': 'token'}):
            return 'A'
        if doc.find('input', {'name': '_token'}):
            return 'A2'
        doc = bs(get('login').text)
        if doc.find('input', {'name': '_token'}):
            return 'B'
        if doc.find('input', {'name': 'email', 'class': 'form-control'}):
            return '5XTO'
        r = get('js/logic.js')
        if "'/create'" in r.text:
            return 'GGGG'
        r = get('auth/signin')
        if '"/auth/signin"' in r.text:
            return 'AdLinkFly'
        r = get('api/v2/health')
        if r.text == 'OK':
            return 'Kutt'
        return None

    url_shortener_class_map = {
        c.__name__.removeprefix(URLShortener.__name__): c
        for c in URLShortener.__subclasses__()
    }

    url_shortener = url_shortener_class_map[URL_SHORTENER_TYPE](**URL_SHORTENER_OPTIONS)

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
