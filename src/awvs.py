import src
"""
Awvs批量爬虫
@author B
"""
# AWVS配置项
cf = src.configparser.ConfigParser()
cf.read("./dicts/autoIncient.ini")
awvs_url = str(cf.get("awvs", "awvs_url"))
scan_speed = str(cf.get("awvs", "scan_speed"))
user_agent = str(cf.get("awvs", "user_agent"))
apikey = str(cf.get("awvs", "apikey"))
headers = {'Content-Type': 'application/json', "X-Auth": apikey}
# xray的监听地址=awvs的代理地址
proxy_address = str(cf.get("xray", "proxy_address"))
proxy_port = int(cf.get("xray", "proxy_port"))

src.urllib3.disable_warnings(src.InsecureRequestWarning)
# 添加扫描任务
def addTask(target):
    try:
        url = ''.join((awvs_url, '/api/v1/targets/add'))
        data = {"targets": [{"address": target, "description": ""}], "groups": []}
        r = src.requests.post(url, headers=headers, data=src.json.dumps(data), timeout=30, verify=False)
        result = src.json.loads(r.content.decode())
        return result['targets'][0]['target_id']
    except Exception as e:
        return e


# 删除全部扫描任务
def delTask():
    while 1:
        quer = '/api/v1/targets'
        try:
            r = src.requests.get(awvs_url + quer, headers=headers, timeout=30, verify=False)
            result = src.json.loads(r.content.decode())
            if int(result['pagination']['count']) == 0:
                print('已删除全部扫描目标。')
                return 0
            for targetsid in range(len(result['targets'])):
                targets_id = result['targets'][targetsid]['target_id']
                targets_address = result['targets'][targetsid]['address']
                try:
                    src.requests.delete(awvs_url + '/api/v1/targets/' + targets_id,
                                        headers=headers,
                                        timeout=30,
                                        verify=False)
                except Exception as e:
                    print(targets_address, e)
        except Exception as e:
            print(awvs_url + quer, e)


# Awvs爬虫
def scan(target, Crawl, profile_id):
    scanUrl = ''.join((awvs_url, '/api/v1/scans'))
    target_id = addTask(target)

    if target_id:
        data = {"target_id": target_id, "profile_id": profile_id, "incremental": False,
                "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
        try:
            configuration(target_id, Crawl)
            response = src.requests.post(scanUrl, data=src.json.dumps(data), headers=headers, timeout=30, verify=False)
            result = src.json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(e)


# 基本配置
def configuration(target_id, Crawl):
    configuration_url = ''.join((awvs_url, '/api/v1/targets/{0}/configuration'.format(target_id)))
    data = {"scan_speed": scan_speed, "login": {"kind": "none"}, "ssh_credentials": {"kind": "none"}, "sensor": False,
            "user_agent": user_agent, "case_sensitive": "auto", "limit_crawler_scope": True, "excluded_paths": [],
            "authentication": {"enabled": False},
            "proxy": {"enabled": Crawl, "protocol": "http", "address": proxy_address, "port": proxy_port},
            "technologies": [], "custom_headers": [], "custom_cookies": [], "debug": False,
            "client_certificate_password": "", "issue_tracker_id": "", "excluded_hours_id": ""}
    r = src.requests.patch(url=configuration_url, data=src.json.dumps(data), headers=headers, timeout=30, verify=False)


def run():
    src.time.sleep(5)
    Crawl = True
    with open('./dicts/targets/live.txt', 'r', encoding='utf-8') as f:
        targets = f.readlines()
    profile_id = "11111111-1111-1111-1111-111111111111"
    if Crawl:
        profile_id = "11111111-1111-1111-1111-111111111117"
    for target in targets:
        target = target.strip().split('>>')[0]
        if scan(target, Crawl, profile_id):
            print("目标 -> {0} 添加成功".format(target))
    print('等待xray扫描完成...')
