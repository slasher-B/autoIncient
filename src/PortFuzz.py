import src
'''
主要用于端口扫描以及联动hydra对一些登录入口进行爆破;
@author B
'''
cf = src.configparser.ConfigParser()
cf.read("./dicts/autoIncient.ini")
timeout = str(cf.get("serverscan", "timeout"))
portStr = str(cf.get("serverscan", "port"))
thread = str(cf.get("hydra", "thread"))
flag = bool(cf.get("hydra", "flag"))
dictPath = src.os.path.abspath('./dicts/dictionaries/' + str(cf.get("hydra", "dictName")))
userDictPath = src.os.path.abspath('./dicts/dictionaries/' + str(cf.get("hydra", "userDict")))
passDictPath = src.os.path.abspath('./dicts/dictionaries/' + str(cf.get("hydra", "passDict")))


# 端口扫描,使用本人魔改的ServerScan_Pro
# 扫描结果将通过本地12345端口用tcp传输,在python端去重写入文件
# 另外有可能出现域名可访问,ip访问不了的情况
def serverScan():
    print('后台开始进行端口扫描，结果输出在./dicts/result/port_scan_report/')
    with open('./dicts/targets/live.txt', 'r') as f:
        for url in f.readlines():
            ip = url.split('>>')[1].strip()
            if ip == '': continue
            src.subprocess.Popen('ServerScan_Pro.exe' +
                                 ' -h ' + ip +
                                 ' -p ' + portStr +
                                 ' -t ' + timeout,
                                 stdout=None,
                                 stderr=src.subprocess.STDOUT,
                                 shell=False)
            with src.socket.socket(src.socket.AF_INET, src.socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', 12345))
                s.listen()
                conn, _ = s.accept()
                with conn:
                    result = list(set(conn.recv(1024).decode('utf-8').split(',')))
            for addr in result:
                host = addr.split(':')[0]
                p = addr.split(':')[1]
                with open('./dicts/result/port_scan_report/' + p, 'a') as inp:
                    inp.write(host + '\n')


# 端口弱口令爆破,工具选择hydra
def hydra():
    print('后台开始进行端口爆破，结果输出在./dicts/result/port_fuzz_report/')
    port = 0
    protocol = ''
    for p in portStr.split(','):
        if p.find('-') != -1:
            tmp = p.split('-')
            '''
            爆破参数配置,web端多数需要验证码,日后编写验证码绕过模块.
            配置里的端口参数如果是范围:    "0-100", 对应的参数配置为po;
            配置里的端口参数如果是单个端口: "100",   对应的参数配置为p;
            '''
            for po in range(int(tmp[0]), int(tmp[1]) + 1):
                if po == 21:port = 21; protocol = 'ftp://'  # ftp
                elif po == 22:port = 22; protocol = 'ssh://'  # ssh
                elif po == 23:port = 23; protocol = 'telnet://'  # telnet
                # elif po == 80:port = 80       # web manager
                # elif po == 81:port = 81
                # elif po == 82:port = 82
                # elif po == 83:port = 83
                # elif po == 84:port = 84
                # elif po == 85:port = 85
                # elif po == 86:port = 86
                # elif po == 87:port = 87
                # elif po == 88:port = 88
                # elif po == 89:port = 89
                elif po == 512:port = 512; protocol = 'rexec://'  # linux rexec
                elif po == 513:port = 513; protocol = 'rexec://'
                elif po == 514:port = 514; protocol = 'rexec://'
                elif po == 5900:port = 5900; protocol = 'vnc://'  # VNC
                elif po == 5901:port = 5901; protocol = 'vnc://'
                elif po == 5902:port = 5902; protocol = 'vnc://'
                # elif po == 8080:port = 8080  # Java-web manager
                # elif po == 8081:port = 8081
                # elif po == 8082:port = 8082
                # elif po == 8083:port = 8083
                # elif po == 8084:port = 8084
                # elif po == 8085:port = 8085
                # elif po == 8086:port = 8086
                # elif po == 8087:port = 8087
                # elif po == 8088:port = 8088
                # elif po == 8089:port = 8089
                else: continue
                hydraRun(port, protocol)
        else:
            p = int(p)
            if p == 25:port = 25; protocol = 'smtp://'  # smtp
            # elif p == 69:port = 69  # tftp
            elif p == 110:port = 110; protocol = 'pop3://'  # pop3
            elif p == 139:port = 139; protocol = 'smb://'  # smb
            elif p == 143:port = 143; protocol = 'imap://'  # imap
            elif p == 389:port = 389; protocol = 'ldap://'  # ldap
            elif p == 445:port = 445; protocol = 'smb://'  # smb
            # elif p == 1194:port = 1194  # open vpn
            # elif p == 1352:port = 1352  # lotus
            elif p == 1433:port = 1433; protocol = 'mssql://'  # sql-server
            # elif p == 1500:port = 1500  # ISPmanager
            # elif p == 1521:port = 1521; protocol = 'oracle-sid://'  # oracle  oracle-listener://
            # elif p == 1723:port = 1723  # pptp
            # elif p == 2082:port = 2082  # cPanel
            # elif p == 2082:port = 2082
            # elif p == 3128:port = 3128  # Squid
            elif p == 3306:port = 3306; protocol = 'mysql://'  # mysql
            # elif p == 3311:port = 3311  # kangle
            # elif p == 3312:port = 3312
            elif p == 3389:port = 3389; protocol = 'rdp://'  # windows rdp
            # elif p == 4848:port = 4848  # GlassFish
            # elif p == 5000:port = 5000  # DB2
            elif p == 5432:port = 5432; protocol = 'postgres://'  # Postgresql
            elif p == 6379:port = 6379; protocol = 'redis://'  # Redis
            # elif p == 7001:port = 7001  # webLogic
            # elif p == 7002:port = 7002
            # elif p == 7778:port = 7778  # Kloxo
            # elif p == 8000:port = 8000  # Ajenti
            # elif p == 8443:port = 8443  # Plesk
            # elif p == 9080:port = 9080  # WebSphere
            # elif p == 9081:port = 9081
            # elif p == 9090:port = 9090
            # elif p == 27017:port = 27017  # MongoDB
            # elif p == 27018:port = 27018
            else:continue
            hydraRun(port, protocol)


def hydraRun(port, protocol):
    if src.os.path.isfile('./dicts/result/port_scan_report/' + str(port)):
        with open('./dicts/result/port_scan_report/' + str(port), 'r') as t:
            if src.os.path.isfile('./dicts/result/port_fuzz_report/hydra.log'):
                src.os.remove('./dicts/result/port_fuzz_report/hydra.log')
            for ip in t.readlines():
                if flag:
                    dict_file = ' -C ' + dictPath
                elif not flag:
                    dict_file = ' -L ' + userDictPath +\
                                ' -P ' + passDictPath
                src.subprocess.Popen('hydra -f -e ns' +
                                     ' -t ' + thread +
                                     ' -s ' + str(port) +
                                     ' -o ' + src.os.path.abspath('./dicts/result/port_fuzz_report/hydra.log') +
                                     dict_file +
                                     ' ' + protocol + ip,
                                     stdout=src.subprocess.PIPE,
                                     stderr=src.subprocess.STDOUT,
                                     shell=False)
    if src.os.path.isfile('./dicts/result/port_scan_report/hydra.log'):
        with open('./dicts/result/port_fuzz_report/hydra.log', 'r') as log:
            while 1:
                line = log.readline()
                if not line:break
                elif line.startswith('['):
                    with open('./dicts/result/port_fuzz_report/hydra_report.log', 'a') as w:
                        w.write(line)
