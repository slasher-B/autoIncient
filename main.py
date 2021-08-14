from src import Auto, awvs, PortFuzz
import src
'''
主程序入口,以及启动xray
@author B
'''
cf = src.configparser.ConfigParser()
cf.read("./dicts/autoIncient.ini")
proxy_address = str(cf.get("xray", "proxy_address"))
proxy_port = str(cf.get("xray", "proxy_port"))


# 启动xray
def xray():
    if src.os.path.isfile('./dicts/result/vul_scan_report.html'):
        print('请先将上次的报告删除或重命名!!')
        return False
    o = src.subprocess.Popen('xray webscan --listen ' + proxy_address + ':' + proxy_port + ' --html-output ./dicts/result/vul_scan_report.html',
                             shell=False,  # 使用系统内建命令时=True
                             stdout=None,  # 命令输出重定向到父进程
                             stderr=src.subprocess.STDOUT)  # 标准错误输出跟随stdout
    try:
        o.wait()
        for i in iter(o.stdout.readline, 'b'):
            if i.decode('gbk').find("'xray'") == 0:
                print('需要将xray添加进环境变量!!')
                break
            elif not i:
                break
            else:
                print(i.decode('gbk'), end='')
    except Exception as e:
        o.kill()


'''
工具分开运行方法：
下面注释描述了功能模块，将对应模块注释掉即可分开运行
'''
if __name__ == '__main__':
    if len(src.sys.argv) != 2:
        print('useagent: python main.py [urlList.txt]')
        src.sys.exit()
    print(src.banner)
    # 首先是url检测部分
    target_file = str(src.sys.argv[1])
    urlList = Auto.readUrlList(target_file)
    for u in urlList:
        Auto.cherkLive(u)
    with src.ProcessPoolExecutor(max_workers=2) as p:
        # 然后是Awvs+Xray扫描部分
        x = p.submit(xray)
        p.submit(awvs.run())
        # 端口扫描 + 高危端口爆破
        p.submit(PortFuzz.serverScan(), PortFuzz.hydra())
        if x.done():awvs.delTask()  # Awvs删除任务
