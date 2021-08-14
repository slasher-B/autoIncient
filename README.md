# autoIncient
这个工具适用于常规渗透项目的漏洞挖掘的初级阶段,联动xray+awvs+serverscan_pro+hydra,支持批量目标扫描。

由于本人魔改了ServerScan的输出方式，因此目前仅支持windows。

# use-agent

pip install -r requirements.txt

编辑配置文件./dicts/autoIncient.ini

python main.py your_targets.txt

# 运行效果


# 工作流程
1.判断目标是否可访问；

2.AWVS + Xray 联动批量扫描；

3.后台用ServerScan_Pro批量扫描端口；

4.在后台联动hydra对端口扫描结果中的地址的高危端口进行针对性爆破,例如:21、22、3306、3389...

（字典可自备,存放目录：./dicts/dictionaries/）
  
5.所有结果均输出在 ./dicts/result/ 下。

# 工作原理

1.访问your_targets.txt中的地址，如果是域名格式则会补全url，最后根据响应状态码判断网站是否存在，
若存在，解析ip并存放在live.txt，不存在则存放在dead.txt；

2.xray开启被动扫描，监听8888端口，awvs设置成爬虫模式，代理设置在xray监听的端口；

3.开启子进程用serverscan对live.txt里解析的ip进行端口扫描，然后对一些高危端口调用hydra进行破解，这些端口可以在代码中自定义。

所有结果都输出在./dicts/result/目录下。

# 其它

在将来会加入验证码绕过模块以及反序列化检测模块。
