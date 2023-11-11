# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time

def mail(subject,text,my_user):
		#self.my_sender='**@163.com'	# 发件人邮箱账号
		#self.my_pass = '****'		   # 发件人邮箱密码(当时申请smtp给的口令)
		my_sender='zhangyan@ccb.fyi'	# 发件人邮箱账号
		my_pass = 'a808067433'		   # 发件人邮箱密码(当时申请smtp给的口令)
		#my_user='liuzhongling@eversec.cn'	  # 收件人邮箱账号
		try:
			msg=MIMEText(text,'HTML','utf-8')
			msg['From']=formataddr(["xx集团",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
			msg['To']=formataddr([my_user,my_user])			  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
			msg['Subject']= subject				# 邮件的主题，也可以说是标题
			#server=smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是80
			server=smtplib.SMTP_SSL("smtp.ccb.fyi", 465)  # 发件人邮箱中的SMTP服务器，端口是80
			server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
			server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
			server.quit()# 关闭连接
			print('发送成功:'+my_user)
		except Exception:# 如果 try 中的语句没有执行
			with open("1.txt","a") as txt:
				txt.write(my_user+"\n")
			print('发送失败:'+my_user)

#mail("常见的网络安全“钓鱼”攻击方式",htmls,)
with open("test.txt") as txt:
	for i in txt:
		i = i.strip()
		#print(i.split("|")[0])
		username = i.split("|")[0]
		tid = i.split("|")[1]
		#htmls = """
		#<div><span style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;">xx创新各位员工:</span></div><div><div style=""><span style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;; white-space: pre;">	</span><font face="lucida Grande, Verdana, Microsoft YaHei">xx集团作为本年度网络安全防护单位，xx创新也在本次活动范围内。为协助集团做好护网行动的防守工作，同时为强网络安全意识，现要求全员对“钓鱼”攻击方式进行学习</font><font face="lucida Grande, Verdana, Microsoft YaHei" style="line-height: 23.8px; font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;">（见此链接:</font><a href="http://110.40.133.150/443283242.html?tid="""+tid+"""\" rel="noopener" target="_blank" style="outline: none; cursor: pointer; color: rgb(30, 84, 148); font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;">什么是网络钓鱼攻击？</a><span style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;">）</span><span style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;">, 以备大家做好自身防范，避免网络安全“钓鱼”攻击。对于活动期间出现因钓鱼邮件导致扣分的个人和集体，集团将给予严肃处理。</span></div></div>
		#"""
		htmls = """<div><div style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;">xx创新各位员工:</div><div style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;"><span style="white-space: pre;">     </span><font face="lucida Grande, Verdana, Microsoft YaHei" style="line-height: 23.8px;">xx集团作为本年度网络安全防护单位，xx创新也在本次活动范围内。为协助集团做好护网行动的防守工作，同时为强网络安全意识，现要求全员对“钓鱼”攻击方式进行学习</font><font face="lucida Grande, Verdana, Microsoft YaHei" style="line-height: 23.8px;">（见此链接:</font><a href="http://110.40.133.150/443283242.html?tid="""+tid+"""\" rel="noopener" target="_blank" style="outline: none; cursor: pointer; color: rgb(30, 84, 148);">什么是网络钓鱼攻击？</a>）, 以备大家做好自身防范，避免网络安全“钓鱼”攻击。对于活动期间出现因钓鱼邮件导致扣分的个人和集体，集团将给予严肃处理。</div></div><div style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;"><br></div><div style="font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;"></div><div style="text-align: right; font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;"><span style="font-family: Arial, Verdana, Geneva, sans-serif;">xxxxxx集团有限公司&nbsp;&nbsp;</span></div><div style="text-align: right; font-family: &quot;lucida Grande&quot;, Verdana, &quot;Microsoft YaHei&quot;;"><span style="font-family: Tahoma, Arial, STHeiti, SimSun;">2022年7月11日&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</span><span style="font-family: Tahoma, Arial, STHeiti, SimSun;">&nbsp;&nbsp;</span></div>"""
		mail("关于了解常见的网络安全“钓鱼”攻击方式的通知",htmls,username)
		time.sleep(10)
