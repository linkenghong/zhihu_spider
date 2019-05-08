# coding=gbk
import requests
from bs4 import BeautifulSoup
import re
import os
import time

def getHTMLText(url, code = "utf-8"): #获取HTML
	try:
		headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"} 
		r = requests.get(url,headers=headers)
		r.raise_for_status()
		r.coding = code
		return r.text
	except:
		return ""
	
def getArtList(artList, columnURL): #获取专栏内文章链接
	html = getHTMLText(columnURL)
	ls = re.findall(r'"url".{0,60}, "comment', html)  #通过网页源代码分析可以知道文章链接在"url"属性内
	for link in ls:
		artList.append(link.split('"')[3])
	
def getImg(artList, fpath): #获取文章内图片地址并下载
	for url in artList[:]:
		html = getHTMLText(url)
		name = url.split('/')[-1] #以文章链接的最后一部分作为名字
		soup = BeautifulSoup(html,'html.parser')
		i = 0 #文章内图片序号
		for link in soup.find_all('figure'):
			match = re.search(r'https://.*?jpg',str(link)) #获取图片地址
			if match:
				downloadImg(match.group(0), fpath, name + '_' + str(i))
				i = i + 1

				
def downloadImg(imgURL, fpath, name): #下载图片
	headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"} 
	path = fpath + name + '.jpg' 
	try:
		if not os.path.exists(fpath):
			os.mkdir(fpath)
		if not os.path.exists(path):
			try:
				r = requests.get(imgURL, headers = headers, timeout = 30)
				if(r.status_code == 200):
					with open(path, 'wb') as f:
						f.write(r.content)
						f.close()
						print(name  + " is saved success!")
				else:
					print(imgURL)
					print(name + "'s status_code is not 200")
			except:
				print(imgURL)
				print(name + " request failed")
		else:
			print(name + " exist")
	except:
		print(imgURL)
		print(name + " failed")
	#time.sleep(1)

	
def main():
	# 专栏url，其中XXX替换成专栏名，即普通链接https://zhuanlan.zhihu.com/XXX的XXX
	# XX替换成要求爬取的文章数，最好是10的整数倍，X替换成从第几篇文章开始爬
	column_url = "https://zhuanlan.zhihu.com/api/columns/XXX/articles?limit=XX&offset=X" 
	#存储地址，其中XX替换成盘符，X替换成路径 ，以专栏名为文件夹名
	output_file = "X://X//" + column_url.split('/')[-2] + "//"
	artList = []  #文章列表
	getArtList(artList, column_url)
	print("The length of artlist is " + str(len(artList))) #要爬取的专栏下文章数
	getImg(artList, output_file)

if __name__ == '__main__':
	main()
