# coding=gbk
import requests
from bs4 import BeautifulSoup
import re
import os
import time

def getHTMLText(url, code = "utf-8"): #获取HTML
	try:
		headers = {"user-agent":"Mozilla/5.0"} 
		r = requests.get(url,headers=headers)
		r.raise_for_status()
		r.coding = code
		return r.text
	except:
		return ""
	
def getArtList(artList, columnURL): #获取专栏内文章链接
	html = getHTMLText(columnURL)
	ls = re.findall(r'"url".{0,60}, "comment', html)  #通过网页源代码分析可以知道文章链接在"url"属性内
	for l in ls:
		artList.append(l.split('"')[3])
	
def getImgList(imgList, artList): #获取文章内图片地址列表
	for url in artList:
		html = getHTMLText(url)
		soup = BeautifulSoup(html,'html.parser')
		for link in soup.find_all('figure'):
			match = re.search(r'https://.*?jpg',str(link))
			if match:
				imgList.append(match.group(0))
				
def downloadImg(imgList, fpath): #下载图片
	headers = {"user-agent":"Mozilla/5.0"} 
	for url in imgList:
		print(url)
		name = url.split('/')[-1]
		path = fpath + name
		try:
			if not os.path.exists(fpath):
				os.mkdir(fpath)
			if not os.path.exists(path):
				try:
					r = requests.get(url, headers = headers)
					with open(path, 'wb') as f:
						f.write(r.content)
						f.close()
						print(name + " is saved success!")
				except:
					print(name + " request failed")
			else:
				print(name + " exist")
		except:
			print(name + " failed")
		time.sleep(1)

	
def main():
	#专栏url，其中XXX替换成专栏名，XX替换成要求爬取的文章数，最好是10的整数倍，X替换成从第几篇文章开始爬
	column_url = "https://zhuanlan.zhihu.com/api/columns/XXX/articles?limit=XX&offset=X" 
	#存储地址，其中XX替换成盘符，X替换成路径 
	output_file = "XX:\X\\"
	artList = []  #文章列表
	imgList = []  #图片列表
	getArtList(artList, column_url)
	print("The length of artlist is " + str(len(artList))) #要爬取的专栏下文章数
	getImgList(imgList, artList)
	print("The length of imglist is " + str(len(imgList))) #要爬取的图片数
	downloadImg(imgList, output_file)

main()
