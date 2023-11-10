import requests
import threading
import queue
from threading import RLock

# 创建 RLock 对象
lock = RLock()

#公共变量与设置
requests.packages.urllib3.disable_warnings()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',}
proxys = {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}  #设置代理
#proxys = {}
suffixFormat = ['.zip', '.rar', '.tar.gz', '.tgz','.7z']
tmp_info_dic = ['1', '2020', '2021', '2022', '2023', 'admin','back',
					'backup', 'bak', 'bin', 'code', 'com', 'data', 'home', 'html', 'local', 'localhost' , 'php',
					 'tar', 'test', 'web', 'www','wwwroot']

thread = 50  #设置线程数量

#检查是否存活
def poc_pocs(host):
	requests.packages.urllib3.disable_warnings()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:76.0) Gecko/20100101 Firefox/76.0',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Accept-Encoding': 'gzip, deflate',
		'Connection': 'close'}
	try:
		zhi = requests.get(host,timeout=10,headers=headers,verify=False,proxies=proxys)
		if "Burp Suite" not in zhi.text and zhi.status_code!=503:
			return True
		return False
	except (requests.exceptions.MissingSchema,requests.exceptions.ConnectTimeout,requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
		return False


#多线程用
def zid(lists):
	words = queue.Queue()
	for i in lists:
		words.put(i)
	return words

#用来保存成功的函数
def save_success(txts):
	with open("success.txt","a") as txt:
		txt.write(txts+"\n")

#用于扫描的函数
def scanurl(url):
	if url[-1:] == "/":
		url = url[:-1]
	chpd = poc_pocs(url)
	if chpd == False:
		print("[-] "+url+" 无法连接！")
		return False
	for bakn in tmp_info_dic:
		for hz in suffixFormat:
			lujin = "{}{}".format(bakn,hz)
			urls = url+"/"+lujin
			#print(urls)
			res = requests.session()
			try:
				r = res.head(urls,headers=headers,timeout=10,verify=False,proxies=proxys)
				if (r.status_code == 200) & ('html' not in r.headers.get('Content-Type')) & (
					'image' not in r.headers.get('Content-Type')) & ('xml' not in r.headers.get('Content-Type')) & (
					'text' not in r.headers.get('Content-Type')) & ('json' not in r.headers.get('Content-Type')) & (
					'javascript' not in r.headers.get('Content-Type')):
					# 上锁
					lock.acquire()
					save_success(urls)
					print("[+] 发现:"+urls)
					# 解锁
					lock.release()
			except:
				pass

def scans(xqueue):
	while True:
		if xqueue.empty():
			return 0
		else:
			i = xqueue.get()
			print("[*] 正在扫描:"+i)
			scanurl(i)

#主函数
def main():
	print("[*] 开始扫描...")
	urllist = []
	with open("url.txt") as txt:
		for i in txt:
			i = i.strip()
			#print(i)
			urllist.append(i)
	print("[*] 总扫描URL数量: "+str(len(urllist)))
	xqueue = zid(urllist)
	threads = []
	for i in range(thread):
		t = threading.Thread(target=scans,args=(xqueue,))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	print("[*] 扫描完成。")

if __name__ == "__main__":
	main()