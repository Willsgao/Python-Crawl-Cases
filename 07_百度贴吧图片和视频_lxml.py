import requests
from lxml import etree

class BaiduSpider(object):
    def __init__(self):
        self.baseurl = 'http://tieba.baidu.com/f?'
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
          
    # 获取帖子链接
    def getPageUrl(self,params):
        res = requests.get(
                self.baseurl,
                params=params,
                headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        # 创建解析对象
        parseHtml = etree.HTML(html)
        # 调用xpath得到列表
        tList = parseHtml.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        # tList:['/p/23023','/p/20302','','']
        for t in tList:
            # 拼接帖子链接
            tLink='http://tieba.baidu.com' \
                    + t
            self.getImgUrl(tLink)
    
    # 获取图片链接
    def getImgUrl(self,tLink):
        # 对帖子链接发请求,获取html
        res=requests.get(tLink,
                headers=self.headers)
        res.encoding='utf-8'
        html=res.text
        # 创建解析对象
        parseHtml=etree.HTML(html)
        # 调用xpath获取图片链接列表
        # 获取视频xpath，需要获取响应内容保存到本地，去分析页面
        imgList=parseHtml.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/img[@class="BDE_Image"]/@src | //div[@class="video_src_wrapper"]/embed/@data-video')
        for imgLink in imgList:
            self.writeImg(imgLink)
    
    # 保存图片到本地
    def writeImg(self,imgLink):
        res=requests.get(imgLink,
                 headers=self.headers)
        res.encoding='utf-8'
        html=res.content
        # 保存图片到本地
        filename=imgLink[-10:]
        with open(filename,'wb') as f:
            f.write(html)
            print('%s下载成功' % filename)

    # 主函数
    def workOn(self):
        name = input('贴吧名:')
        begin = int(input('起始页:'))
        end = int(input('终止页:'))
        for i in range(begin,end+1):
            pn = (i-1)*50
            # 定义查询参数
            params = {
                'kw' : name,
                'pn' : str(pn)
            }
            self.getPageUrl(params)
        
if __name__ == '__main__':
    spider = BaiduSpider()
    spider.workOn()














