from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pickle
import time
class Item:
    def __init__(self,url,name):
        self.url = url
        self.name = name

tlist = [
    Item('/','首页'),
    Item('/resume/','介绍'),
    Item('/adder/','加法器'),
]

with open('./data/NewsLib.pkl','rb')as file:
    NewsLib = pickle.load(file)


def resume(request):

    dic = {
        'tutorial_list' : tlist,
    }
    return render(request,'resume.html',dic)    

def adder(request):
    dic = {
        'tutorial_list' : tlist,
    }
    return render(request,'adder.html',dic)

def page(request):
    num = int(request.path[6:])
    news = NewsLib[num]

    paragraphs = news.text.split('\n')
    text = []
    for paragraph in paragraphs:
        p = paragraph.strip()
        if p == '':
            continue
        else:
            text.append(p)

    r_news = []
    for i in range(min(8,len(news.similar))):
        rnews = NewsLib[news.similar[i]]
        r_news.append(Item("/page/{}".format(rnews.id),rnews.title))

    dic = {
        'tutorial_list': tlist + [Item(news.url,'原网址')],
        'web_title': news.title+" 天网搜索",
        'title': news.title,
        'subtitle': '日期：{} 来源：{}'.format(news.date,news.source),
        'text': text,
        'related_news': r_news,
    }
    return render(request,'text.html',dic)

class News:
    def __init__(self,url,title,summary):
        self.url = url
        self.title = title
        self.summary = summary

def search(request):

    if 'input_text' not in request.GET:
        return HttpResponseRedirect(r'/')
    input_text = request.GET['input_text']
    if 'page_num' in request.GET:
        page_num = int(request.GET['page_num'])
    else:
        page_num = 1
    def get_search_results(st,ed,text):
        if text == '':
            return list(range(st,ed))
        Ans = set()
        for i in range(st,ed):
            news = NewsLib[i]
            if news.title.find(text)!=-1 or news.abstract.find(text)!=-1:
                Ans.add(i)
        for i in range(st,ed):
            if len(Ans)<=200:
                news = NewsLib[i]
                if news.text.find(text)!=-1:
                    Ans.add(i)
            else:
                break
        Ans = list(Ans)
        Ans.sort()
        return Ans

    time_st = time.time()

    newslist = get_search_results(0,len(NewsLib),input_text)

    if len(newslist)<=(page_num-1)*10:
        return HttpResponse(r"Error! We don't have enough results!")
    stpos = (page_num-1)*10
    edpos = min(10*page_num,len(newslist))

    time_ed = time.time()
    newslt = []
    for i in range(stpos,edpos):
        news = NewsLib[newslist[i]]
        newslt.append(News("/page/{}".format(news.id),news.title,news.abstract))
    page_num_bef = max(1,page_num-4)
    page_num_aft = min(int((len(newslist)-1)/10+1),page_num+4)
    page_total = [Item("/search?input_text={}&page_num={}".format(input_text,num),str(num)) for num in range(page_num_bef,page_num_aft+1)]
    dic = {
        'tutorial_list': tlist,
        'web_title':request.GET['input_text'] + " 搜索结果",
        'search_count': str(len(newslist)),
        'search_time': str(time_ed-time_st), 
        'news': newslt,
        'page_total': page_total,
    }
    return render(request,'search.html',dic)



def home(request):
    if 'input_text' in request.GET:
        return search(request)
    else:
        return render(request,'home_page.html',{})
