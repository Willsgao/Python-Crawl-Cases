import requests
import pymysql
import json
import time

class DoubanSpider(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?'
        self.headers = {'User-Agent':'Mozilla/5.0'}
        # 数据库对象(doubandb)
        self.db = pymysql.connect('172.40.91.200',
                                  'lion','123456',
                                  'doubandb',
                                  charset='utf8')
        # 游标对象
        self.cursor = self.db.cursor()
    # 获取页面
    def getPage(self,params):
        res = requests.get(self.url,params=params,
                           headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        self.parsePage(html)

    # 解析页面
    def parsePage(self,html):
        # 把json格式的响应内容转为Python数据类型
        hList = json.loads(html)
        # hList : [{电影1信息},{电影2信息},{}]
        for h in hList:
            name = h['title']
            score = h['score']
            # actors : ['张国荣','张曼玉','']
            actors = h['actors']
            L = [name,float(score.strip()),','.join(actors)]
            self.writeMysql(L)

    # 保存到mysql数据库
    def writeMysql(self,L):
        ins = 'insert into film(name,score,actors)\
              values(%s,%s,%s)'
        self.cursor.execute(ins,L)
        self.db.commit()

    # 主函数
    def workOn(self):
        print('\033[31m*********************\033[0m')
        print('  |剧情|喜剧|爱情|  ')
        print('\033[31m*********************\033[0m')
        kinds = ['剧情','喜剧','爱情']
        kind = input('请输入电影类型:')
        kDict = {'剧情':'11','喜剧':'24','爱情':'13'}
        if kind in kinds:
            n = input('请输入要爬取的电影数量:')
            params = {
                    "type" : kDict[kind],
                    "interval_id" : "100:90",
                    "action" : "",
                    "start" : "0",
                    "limit" : n
            }
            self.getPage(params)
            print('爬取成功，数量：%s' % n)
        else:
            print('类型不存在!')
if __name__ == '__main__':
    start = time.time()
    spider = DoubanSpider()
    spider.workOn()
    end = time.time()
    print('执行时间:%.2f' % (end - start))








