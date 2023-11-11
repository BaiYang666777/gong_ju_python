import requests
import base64
import mmh3

proxys = {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}


def b64bm(strs):#用于对字符串进行base64编码
	strsb = base64.encodebytes(strs)
	return strsb
def get_faviconhash(url):#用于获取favicon的hash值
	global proxys
	url = url.strip()
	if url[-1:] == "/":
		url = url[:-1]
	url = url+"/favicon.ico"
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
		}
		requests.packages.urllib3.disable_warnings()
		res = requests.session()
		response = res.get(url,headers=headers,timeout=10,verify=False,proxies=proxys)
		favicon = b64bm(response.content)
		favicon_hash = str(mmh3.hash(favicon))
		return favicon_hash
	except (requests.exceptions.ConnectTimeout,requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout,requests.exceptions.ChunkedEncodingError):
		return None

z = get_faviconhash("https://x.x.x.x/")
print(z)