import socket


def redisscan(ip,port):
	payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
	s = socket.socket()
	socket.setdefaulttimeout(10)
	#try:
	s.connect((ip,int(port)))
	s.sendall(payload.encode())
	jieguo = s.recv(1024).decode()
	if jieguo and 'redis_version' in jieguo:
		print("[+]"+ip+":"+str(port)+"\t存在未授权访问！！")
	#except:
	else:
		print("[-]"+ip+":"+str(port)+"\t不存在未授权访问")
#redisscan("118.89.109.106","6379")

with open("1.txt") as txt:
	for i in txt:
		i = i.strip()
		dk
		ip
		redisscan(ip,dk)