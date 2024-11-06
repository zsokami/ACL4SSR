import os

import requests

session = requests.Session()
session.headers['X-Apikey'] = os.getenv('VIRUSTOTAL_API_KEY')


def subdomains(domain):
    resp = session.get(f'https://www.virustotal.com/api/v3/domains/{domain}/subdomains?limit=1000')
    if not resp.ok:
        raise Exception(resp.status_code, resp.text)
    return [x['id'] for x in resp.json()['data'] if 'attributes' in x and any(
        r['type'][0] == 'A' for r in x['attributes']['last_dns_records'])]


def sub(domain, fn=None):
    return '\n'.join(f'0.0.0.0 {x}' for x in subdomains(domain) if not fn or fn(x))


hosts = f'''127.0.0.1       localhost
::1             ip6-localhost

# 某些影视/动漫 APP 广告拦截规则

dc.sigmob.cn

{sub('ugdtimg.com')}

0.0.0.0 open.e.kuaishou.com

0.0.0.0 open.e.kuaishou.cn

{sub('adkwai.com')}

{sub('adukwai.com')}

{sub('e.qq.com')}

{sub('gdt.qq.com')}

0.0.0.0 gray.i.gdt.qq.com
0.0.0.0 q.i.gdt.qq.com

0.0.0.0 gray.v.gdt.qq.com

{sub('pangolin-sdk-toutiao.com')}

{sub('pangolin-sdk-toutiao-b.com')}

0.0.0.0 api-access.pangolin-sdk-toutiao1.com

{sub('snssdk.com', lambda x: x.startswith(('pangolin', 'tnc')))}

{sub('zijieapi.com', lambda x: x.startswith(('tnc')))}

{sub('pglstatp-toutiao.com')}

{sub('ctobsnssdk.com')}

0.0.0.0 api.hzsanjiaomao.com

0.0.0.0 api.juliangcili.com

{sub('anythinktech.com')}

0.0.0.0 utoken.umeng.com
0.0.0.0 ulogs.umeng.com

0.0.0.0 mobads.baidu.com
0.0.0.0 mobads-logs.baidu.com
0.0.0.0 als.baidu.com
0.0.0.0 hmma.baidu.com
'''

with open('hosts', 'w') as f:
    f.write(hosts)
