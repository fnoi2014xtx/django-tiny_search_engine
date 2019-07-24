import pickle
from crawler import News

NewsLib = set()
NewsList = []

class FormatNews:
	def __init__(self,news,idnum):
		self.title = news.title
		self.abstract = news.abstract
		self.date = news.date
		self.source = news.source
		self.text = news.text
		self.url = news.link
		self.id = idnum
		self.keyword = {}
		self.similar = []

if __name__ == '__main__':

	with open('News.pkl','rb')as file:
		NewsLib = pickle.load(file)

	for news in NewsLib:
		date = news.date[0:4]+news.date[5:7]+news.date[8:10]
		news.date = date
		NewsList.append(news)

	NewsList.sort(key = lambda news:int(news.date))
	
	FormatNewsList = []
	
	total = len(NewsList)
	
	for i in range(total):
		FormatNewsList.append(FormatNews(NewsList[i], i))
	
	with open('FormatNews.pkl','wb')as File:
		pickle.dump(FormatNewsList,File)

