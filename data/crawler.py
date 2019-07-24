import requests
import re
from bs4 import BeautifulSoup
import json
import pickle
from lxml import etree
import time
class News:

	def __init__(self,title,date,source,text,abstract,link):
		self.title = title
		self.date = date
		self.source = source
		self.text = text
		self.link = link
		self.abstract = abstract

'''
def PrintNewsLibrary():
	for news in NewsLibrary:
		print("=================="+news.title+"=======================")
		print("date = ",news.date)
		print("source = ",news.source)
		print("link = ",news.link)
		print("abstract = ",news.abstract)
		print("text = ",news.text)
'''
def crawl_xinhua():
	NewsLibrary = set()
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Host': 'qc.wa.news.cn',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}


	nidlist = [113352,113321,113207,11147664,11109063]
	rootlinklist = ['http://qc.wa.news.cn/nodeart/list','http://qc.wa.news.cn/nodeart/list','http://qc.wa.news.cn/nodeart/list','http://qc.wa.news.cn/nodeart/list','http://qc.wa.news.cn/nodeart/list']
#	rootlinklist = ['http://da.wa.news.cn/nodeart/page']

	str1 = '?nid='
	str2 = '&pgnum='
	str3 = '&cnt=10&tp=1&orderby=1?callback=jQuery112409186225959739442_1536632034874&_=1536632034876'


	def GetText(link):
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Host': 'www.xinhuanet.com',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
		}

		headers2 = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Host': 'education.news.cn',
			'Referer': 'http://education.news.cn/',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		}
		if link.startswith("http://education.news.cn"):
			headers = headers2
		r = requests.get(link,headers = headers)
	#	time.sleep(0.1)
		soup = BeautifulSoup(r.content.decode('UTF-8'),"html.parser")
		textnode = soup.find("div",id = "p-detail")
		if textnode == None:
			return "" 
	#	print(r.content.decode('UTF-8'))
	#	print(textnode)
		graphnodes = textnode.find_all("p")
		if graphnodes == None:
			return ""
		text = ""
		for graphnode in graphnodes:
			text += graphnode.text.strip()+'\n'+'\n'
	#	print(text)
		return text

#	GetText("http://www.xinhuanet.com/science/2018-09/09/c_137452149.htm")

	for i in range(5):
		NewsLibrary = set()
		_rootlink = rootlinklist[i]
		_rootlink += str1 + str(nidlist[i])
		for j in range(1,101):
	#	for j in range(1,2):
			rootlink = _rootlink + str2 + str(j) + str3
			print(rootlink)
			jsonstr = requests.get(rootlink,headers = headers).text
		#	time.sleep(0.1)
			id1 = jsonstr.find("{")
			id2 = jsonstr.rfind(")")
			jsonstr = jsonstr[id1:id2]
		#	print(jsonstr)
			jsondata = json.loads(jsonstr)
			NewsInfoList = jsondata["data"]["list"];
			for NewsInfo in NewsInfoList:
				Title = NewsInfo["Title"]
				Date = NewsInfo["PubTime"]
				Link = NewsInfo["LinkUrl"]
				Source = NewsInfo["SourceName"]
				Abstract = NewsInfo["Abstract"]
				if (not Link.startswith("http://www.xinhuanet.com")) and (not Link.startswith("http://education.news.cn")):
					continue
				print(Link)
				Text = GetText(Link)
				if(Text==""):
					continue
				print(Title)
			#	print(Link)value, ..., sep, end, file, flush
				NewsLibrary.add(News(Title, Date, Source, Text, Abstract,Link))
		with open("news1"+str(i)+".pkl", "wb") as f:
			pickle.dump(NewsLibrary,f)
		print(len(NewsLibrary))
#	PrintNewsLibrary()


def crawl_renmin():
	NewsLibrary = set()
	rootlinklist = [
		'http://politics.people.com.cn',
		'http://world.people.com.cn',
		'http://finance.people.com.cn',
		'http://tw.people.com.cn',
		'http://military.people.com.cn',
		'http://opinion.people.com.cn',
		'http://leaders.people.com.cn',
		'http://legal.people.com.cn',
		'http://society.people.com.cn',
		'http://industry.people.com.cn',
		'http://sports.people.com.cn',
		'http://scitech.people.com.cn',
	]

	LinkLibrary = set()
	StartLinkList = []
	
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Host': None,
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}

#	print('!!!!!!!!!!!!!')


	def GetStartLink(rootlink,html):
	#	print(html)
		soup = BeautifulSoup(html,'html.parser')
		nodes = soup.find_all("div",class_ = "hdNews clearfix")
		for node in nodes:
		#	print(node)
			suf = node.find('a').get('href')
			link = rootlink + suf
			if suf.startswith('http://'):
				link = suf
			StartLinkList.append(link)
		#	print(link)



	for _rootlink in rootlinklist:
		id1 = _rootlink.find('//')+2
		headers['Host'] = _rootlink[id1:]
		print(headers['Host'])
		for i in range(1,7):
			rootlink = _rootlink+'/index'+str(i)+'.html#fy01'
		#	print(rootlink)
			r = requests.get(rootlink,headers = headers)
		#	time.sleep(0.1)
			if r.status_code != 200:
				break
			r.encoding = 'gb2312'
		#	print(r.text)
			GetStartLink(_rootlink,r.text)
	
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	}
	
	def Dfs(link,depth):
	#	if(len(LinkLibrary)>=1000):
	#		return
		if link in LinkLibrary:
			return
		print(link,'Dfs start')
		#headers['Host'] = link[:link.find('/')]
		try:	
			r = requests.get(link,headers = headers,timeout = 5)
		#	time.sleep(0.1)
		except Exception as e:
			return
		if r.status_code!=200:
			return
		print(depth,len(LinkLibrary),link)
		LinkLibrary.add(link)
		if(depth>=2):
			return
		r.encoding = 'gb2312'
		html = r.text
	#	print(html)
		if html.find('<!--相关新闻-->')==-1:
			return

		soup = BeautifulSoup(html,"html.parser")
		NewsBox = soup.find('div',class_ = 'clearfix box_news')
		if NewsBox==None or NewsBox.h2.text!='相关新闻':
			return
		nodelist = NewsBox.find_all('a')
		linklist = [node.get('href') for node in nodelist]
		print(link,'Dfs end')
		for url in linklist:
			Dfs(url, depth+1)
	

#	Dfs('http://leaders.people.com.cn/n1/2018/0904/c58278-30269871.html', 0) 
	for startlink in StartLinkList:
		Dfs(startlink,0)

	print(len(LinkLibrary))

	def CreateNews(link):
		print(link,"CreateNews")
		try:
			r = requests.get(link,headers = headers,timeout=5)
		#	time.sleep(0.1)
		except Exception as e:
			return
		r.encoding = 'gb2312'
		html = r.text
	#	print(html)
		html = etree.HTML(r.text)
		Title = html.xpath('/html/body/div/h1')
		if Title == []:
			return
		Title = Title[0].text
		DateAndSource = html.xpath('/html/body/div/div[@class="box01"]/div[@class="fl"]')
		if DateAndSource == []:
			return
		Date = DateAndSource[0].xpath('text()')[0][:-5]
		Source = DateAndSource[0].xpath('a/text()')
		if Source == []:
			Source = 'UNKNOWN'
		else:
			Source = Source[0]
		TextList = html.xpath('/html/body/div/div[@class="fl text_con_left"]/div[@class="box_con"]/p')

		textList = []

		for text in TextList:
			if text.xpath("strong")!=[]:
				textList+=text.xpath('strong/text()')
			else:
				textList+=text.xpath('text()')
	#	print(textList)
		def notblank(s):
			return s.strip()!=''
		textList = list(filter(notblank, textList))
	#	print(textList)
		if textList == []:
			return
		Abstract = textList[0]
		Text = ""
		for text in textList:
			Text += text+'\n'
		NewsLibrary.add(News(Title, Date, Source, Text, Abstract, link))
		print(link,"CreateNews End")

#	CreateNews('http://politics.people.com.cn/n1/2018/0724/c1001-30166348.html')
	num = 0
	n = 0
	for link in LinkLibrary:
		CreateNews(link)
		num += 1
		if num == 1000:
			with open("news2"+str(n)+".pkl", "wb") as f:
				pickle.dump(NewsLibrary,f)
			n += 1
			NewsLibrary = set()
			num = 0
#	with open("news2.pkl", "wb") as f:
#		pickle.dump(NewsLibrary,f)
#	print(len(NewsLibrary))
#	PrintNewsLibrary()
		


if __name__ == '__main__':

	crawl_xinhua()
	crawl_renmin()



