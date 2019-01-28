import urllib.request
import re 
import csv
import time 

class MaoyanSpider(object):
    def __init__(self):
        self.baseurl = 'https://maoyan.com/board/4?offset='
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        self.page = 1
        
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
        self.writeCsv(rList)
    
    # 保存数据
    def writeCsv(self,rList):
        with open('猫眼.csv','a',newline='',encoding='gb18030') as f:
            # 创建写入对象
            writer = csv.writer(f)
            for rt in rList:
                # 此方法去左右两侧空白麻烦
                #info = list(rt)
                info = [
                        rt[0].strip(),
                        rt[1].strip(),
                        rt[2].strip()
                    ]
                # 在csv文件写入数据
                writer.writerow(info)

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
    
    
    
    
    
    
    
    
    
    
    
