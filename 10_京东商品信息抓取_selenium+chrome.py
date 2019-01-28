from selenium import webdriver
import time
import csv

# 创建浏览器对象
driver = webdriver.Chrome()
# 向京东首页发请求
driver.get('https://www.jd.com/')
# 发送文字到搜索框
key = input('请输入商品:')
driver.find_element_by_class_name('text').send_keys(key)
# 点击搜索按钮
driver.find_element_by_class_name('button').click()
time.sleep(2)
n = 1
# while True:
for i in range(3):
    # 执行JS脚本,进度条拉到最下面
    driver.execute_script(
        'window.scrollTo(0,document.body.scrollHeight)'
    )
    # 给页面加载留出时间
    time.sleep(3)
    # 基准xpath，每个商品的节点对象列表
    rList = driver.find_elements_by_xpath('//div[@id="J_goodsList"]/ul/li')
    for r in rList:
        info = r.text.split('\n')
        # ￥52.80
        # Python编程从入门到实践python3.0绝技核心编程基础教程网络爬虫入门书籍
        # 500 + 条评价
        # 润知天下图书专营店
        price = info[0]
        if info[1] != '拍拍':
            name = info[1]
            commit = info[2]
            market = info[3]
        else:
            name = info[2]
            commit = info[3]
            market = info[4]
        L = [price, commit, market, name]
        # 存入csv文件
        with open('京东.csv','a',newline='',encoding='gb18030') as f:
            writer = csv.writer(f)
            writer.writerow(L)
    print('第%d页爬取成功' % n)
    n += 1
    # 点击下一页
    if driver.page_source.find('pn-next disabled') == -1:
        driver.find_element_by_class_name('pn-next').click()
        time.sleep(2)
    else:
        break








