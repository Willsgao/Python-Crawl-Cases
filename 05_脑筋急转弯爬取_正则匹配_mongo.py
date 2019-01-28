import requests
import re 
import pymongo

class NeihanSpider(object):
    def __init__(self):
        self.baseurl = 'https://www.neihan8.com/njjzw/'
        self.headers = {'User-Agent':'Mozilla/5.0'}
        self.proxies = {}
        # 三个对象
        self.conn = pymongo.MongoClient(
                         '192.168.56.131',
                          27017)
        self.db = self.conn['neihandb']
        self.myset = self.db['njjzw']
    
    # 下载页面
    def getPage(self,url):
        res = requests.get(url=url,
                headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        self.parsePage(html)
    
    # 解析页面
    def parsePage(self,html):
        p = re.compile('<div class="text-column-item.*?title=.*?>(.*?)</a>.*?<div class="desc">(.*?)</div>',re.S)
        rList = p.findall(html)
        # rList:[('问题','答案'),()]
        self.writeMongo(rList)
        
    # 保存到mongodb
    def writeMongo(self,rList):
        for rt in rList:
            d = {
                'question' : rt[0].strip(),
                'answer' : rt[1].strip()
              }
            # 插入mongo数据库
            self.myset.insert_one(d)
    
    # 主函数
    def workOn(self):
        menu = '''
            \033[31m**********************
            ----   1.爬取     ----
            ----   2.退出     ----
            **********************
            请选择(1/2):\033[0m'''
        cmd = input(menu)
        if cmd.strip() == '1':
            n = input('请输入页数:')
            if n.strip().isdigit():
                n = int(n)
                # 用户输入1是一种情况
                if n == 1:
                    self.getPage(self.baseurl)
                    print('第1页爬取成功')
                else:
                    self.getPage(self.baseurl)
                    print('第1页爬取成功')
                    for pg in range(2,n+1):
                        # 拼接URL
                        url = self.baseurl\
                              + 'index_' +\
                              str(pg) +\
                              '.html'
                        self.getPage(url)
                        print('第%d页爬取成功' % pg) 
            else:
                print('请输入1-175的整数')
        else:
            print('爬取结束,谢谢使用')
        
        
        
        
        
        

if __name__ == '__main__':
    spider = NeihanSpider()
    spider.workOn()
    
    
#   1.爬取
#     爬取页数
#   2.退出   
    
    
    
    
    
    
    
    