# -*- coding: UTF-8 -*-
import requests
import MySQLdb
from bs4 import BeautifulSoup as sp
import re
url='https://www.toutiao.com/search_content/'

param={'offset': '0', 'format': 'json', 'keyword': '大数据', 'count':'20'}

patterns='http://toutiao.com/group/\w+/'

cookies = {'tt_webid':'6531682658672903687'}

user_agent = 'Mozilla/5.0 (X11;Ubuntu;Linux x86_64; rv<br>:40.0) Gecko/20100101 Firefox/40.0'

headers={'User-agent':user_agent}


#num>=20起，为想获得的链接数量，keyword是搜索关键词
def get_article_by_search(num,keyword):
    param['keyword']=keyword
    offset=0
    rearticles=[]
    while True:
        articles = requests.get(url, params=param).json()['data']
        for article in articles:
            try:
                rearticles.append({'title':article['title'],'url':article['article_url']})
            except Exception:
                print('get error')
        if num>offset:
            offset=offset+20
            param['offset']=offset
        else:
            break
    return rearticles

#拼接文章模块
def join_article(article):
    try:
        response=requests.post(article['url'],cookies=cookies,headers=headers)
        data=get_data(response)
        return dict(data.items()+{'url':article['url'],'title':article['title']}.items())
    except Exception:
        print 'join error'

#从response中提取内容
def get_data(response):
    data=sp(response.content,'lxml')
    text = str(data.findAll('script')[6])
    try:
        CandT=text.split('\n')
        content=CandT[20].strip().replace('content: ','')
        tag=CandT[30].strip().replace('tags: ','')
        tag=re.sub('name|{|}|"|:|\[|\]','',tag)[:-1]
        return {'content':content,'tag':tag}
    except Exception:
        return None

#一次整合存入数据
def inter_cache_in_mysql(num,keyword):
    articles=get_article_by_search(num,keyword)
    whole_article=[]
    for article in articles:
        whole_article.append(join_article(article))
    try:
        connect=MySQLdb.connect(user='root',db='toutiaocrawl',charset='utf8')
        cur=connect.cursor()
    except Exception:
        print 'cannot get database connection'
    for i in whole_article:
        try:
            title=i['title'].encode('utf-8')
            print(title)
            url=i['url']
            print(url)
            content=i['content']
            print(content)
            tag=i['tag']
            print(tag)
            insertMysql = 'insert into article VALUES ("{0}","{1}","{2}","{3}")'.format(title,url,content,tag)
            print(insertMysql)
            cur.execute(insertMysql)
        except Exception:
            print('insert error')

    cur.close()
    connect.commit()
    print 'finished'










if __name__ == '__main__':
    keyword=['数据挖掘','机器学习','大数据','php','java','mysql','c语言','数据库','云计算','区块链','tensorflow','keras','javascript']
    for i in keyword:
        inter_cache_in_mysql(150,i)







