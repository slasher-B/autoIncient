import src
'''
检查网站是否能够访问
@author B
'''
# 读取目标资产,规范化url
def readUrlList(fname):
    lines = []
    with open(fname, 'r', encoding='UTF-8') as f:
        for line in f:
            if not line.startswith('#'):
                ls = line.strip('\n').replace(' ', '')
                if not ls.startswith('http'):
                    ls = 'http://' + ls
                lines.append(ls)
    return lines


# 将有效的url和解析成ip的域名写入文件
def writeTo(fname, u):
    host = str(u).split("/")[2]
    if fname == 'live.txt':
        if not src.re.match(
                '^(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))$',
                host):
            host = src.socket.gethostbyname(host)
        with open('./dicts/targets/' + fname, 'a') as f:
            f.write(u + '>>' + host + '\n')
    elif fname == 'dead.txt':
        with open('./dicts/targets/' + fname, 'a') as f:
            f.write(u + '\n')


# 检查可访问的url
def cherkLive(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4482.0 Safari/537.36 Edg/92.0.874.0',
    }
    s = src.requests.session()
    s.keep_alive = False
    try:
        resp = s.get(url=url, headers=headers, timeout=(2, 3))
        if resp.status_code != 404:
            writeTo('live.txt', url)
        else:
            writeTo('dead.txt', url)
    except Exception as e:
        u = url.replace('http', 'https')
        try:
            print('转换为https -> ' + u)
            r = src.requests.get(url=u, headers=headers, timeout=(3, 5))
            if r.status_code != 404:
                writeTo('live.txt', u)
            else:
                writeTo('dead.txt', u)
        except Exception as er:
            writeTo('dead.txt', u)
