import urllib.request
import re 
import pymongo
import time 

class MaoyanSpider(object):
    def __init__(self):
        self.baseurl = 'https://maoyan.com/board/4?offset='
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        self.page = 1
        # 连接对象
        self.conn = pymongo.MongoClient(
                         '192.168.56.131',
                         27017)
        # 库对象
        self.db = self.conn['mydb']
        # 集合对象
        self.myset = self.db['top100']
        
    # 获取页面
    def getPage(self,url):
        # 三步走
        req = urllib.request.Request(url,
                   headers=self.headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        self.parsePage(html)
        
    # 解析页面
    def parsePage(self,html):
        p = re.compile('<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>',re.S)
        rList = p.findall(html)
        # rList:[('霸王别姬','张国荣','1993-'),(),()]
        self.writeMongo(rList)
    
    # 保存数据
    def writeMongo(self,rList):
        for rt in rList:
            d = {
                "name" : rt[0].strip(),
                "star" : rt[1].strip(),
                "time" : rt[2].strip()
              }
            # 插入到mongo数据库
            self.myset.insert_one(d)

    # 主函数
    def workOn(self):
        for pg in range(0,21,10):
            url = self.baseurl+str(pg)
            self.getPage(url)
            print('第%d页爬取成功' % self.page)
            time.sleep(3)
            self.page += 1

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.workOn()
    
    
    
    
    
    
    
    
    
    
    
