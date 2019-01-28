import requests
from lxml import etree
import pymongo

class QiushiSpider(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/text/page/4/'
        self.headers = {'User-Agent':'Mozilla/5.0'}
        # 连接对象
        self.conn = pymongo.MongoClient(
                        'localhost',27017)
        # 库对象
        self.db = self.conn['qiushidb']
        # 集合对象
        self.myset = self.db['baike']

    # 获取页面
    def getPage(self):
        res = requests.get(self.url,
                        headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text 
        self.getParsePage(html)

    # 解析页面和保存页面
    def getParsePage(self,html):
        # 创建解析对象
        parseHtml = etree.HTML(html)
        # 基准xpath,匹配每个段子的节点对象列表
        baseList = parseHtml.xpath('//div[contains(@id,"qiushi_tag_")]')
        # 遍历每个段子节点对象
        for base in baseList:
            # 用户昵称, 节点对象.text属性可获取该节点文本内容
            name = base.xpath('./div/a/h2')
            if not name:
                name = '匿名用户'
            else:
                name = name[0].text
            # 段子内容
            content = base.xpath('.//div[@class="content"]/span')[0].text
            # 好笑数量
            laughNum = base.xpath('.//i[@class="number"]')[0].text
            # 评论数量
            pingNum = base.xpath('.//i[@class="number"]')[1].text

            # 存入数据库
            d = {
                "name" : name,
                "content" : content,
                "laughNum" : laughNum,
                "pingNum" : pingNum
            }
            self.myset.insert_one(d)

    
    # 主函数
    def workOn(self):
        self.getPage()

if __name__ == '__main__':
    spider = QiushiSpider()
    spider.workOn()
    
