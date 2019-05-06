# coding=gbk
import requests
from bs4 import BeautifulSoup
import re
import os
import time

def getHTMLText(url, code = "utf-8"): #��ȡHTML
	try:
		headers = {"user-agent":"Mozilla/5.0"} 
		r = requests.get(url,headers=headers)
		r.raise_for_status()
		r.coding = code
		return r.text
	except:
		return ""
	
def getArtList(artList, columnURL): #��ȡר������������
	html = getHTMLText(columnURL)
	ls = re.findall(r'"url".{0,60}, "comment', html)  #ͨ����ҳԴ�����������֪������������"url"������
	for l in ls:
		artList.append(l.split('"')[3])
	
def getImgList(imgList, artList): #��ȡ������ͼƬ��ַ�б�
	for url in artList:
		html = getHTMLText(url)
		soup = BeautifulSoup(html,'html.parser')
		for link in soup.find_all('figure'):
			match = re.search(r'https://.*?jpg',str(link))
			if match:
				imgList.append(match.group(0))
				
def downloadImg(imgList, fpath): #����ͼƬ
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
	#ר��url������XXX�滻��ר������XX�滻��Ҫ����ȡ���������������10����������X�滻�ɴӵڼ�ƪ���¿�ʼ��
	column_url = "https://zhuanlan.zhihu.com/api/columns/XXX/articles?limit=XX&offset=X" 
	#�洢��ַ������XX�滻���̷���X�滻��·�� 
	output_file = "XX:\X\\"
	artList = []  #�����б�
	imgList = []  #ͼƬ�б�
	getArtList(artList, column_url)
	print("The length of artlist is " + str(len(artList))) #Ҫ��ȡ��ר����������
	getImgList(imgList, artList)
	print("The length of imglist is " + str(len(imgList))) #Ҫ��ȡ��ͼƬ��
	downloadImg(imgList, output_file)

main()
