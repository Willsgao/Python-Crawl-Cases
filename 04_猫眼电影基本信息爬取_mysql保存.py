import urllib.request
import re 
import pymysql
import time 
import warnings

class MaoyanSpider(object):
    def __init__(self):
        self.baseurl = 'https://maoyan.com/board/4?offset='
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        self.page = 1
        # 创建数据库对象
        self.db = pymysql.connect(
                    '192.168.56.131',
                    'lion','123456','mydb',
                    charset='utf8')
        # 创建游标对象
        self.cursor = self.db.cursor()
      
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
        self.writeMysql(rList)
    
    # 保存数据
    def writeMysql(self,rList):
        # 忽略警告
        warnings.filterwarnings('ignore')
        ins = 'insert into top100(name,star,\
               time) values(%s,%s,%s)'
        for rt in rList:
            L = [
                    rt[0].strip(),
                    rt[1].strip(),
                    rt[2].strip()[5:15]
                ]
            # execute要使用列表传参
            self.cursor.execute(ins,L)
            self.db.commit()

    # 主函数
    def workOn(self):
        for pg in range(0,11,10):
            url = self.baseurl+str(pg)
            self.getPage(url)
            print('第%d页爬取成功' % self.page)
            time.sleep(3)
            self.page += 1
        # 等所有页面爬完后再关闭数据库
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.workOn()
    
    
    
    
    
    
    
    
    
    
    
