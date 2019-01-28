import json
import time
import random
import hashlib
import requests

# F12或抓包工具抓到的POST的地址
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
key = input('请输入要翻译的内容:')
# 获取salt的值
salt = int(time.time()*1000)+\
                   random.randint(0,10)
# 获取sign的值
sign = "fanyideskweb" + key + str(salt) +\
                     "p09@Bn{h02_BIEe]$P^nG" 
s = hashlib.md5()
s.update(sign.encode('utf-8'))
sign = s.hexdigest()

# 获取ts
ts = int(time.time()*1000)

# 定义headers
headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        #Accept-Encoding: gzip, deflate
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'255',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'OUTFOX_SEARCH_USER_ID=1516386930@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=760569518.7197; JSESSIONID=aaa9667LaTZN783i7g-Hw; td_cookie=18446744073249454972; ___rl__test__cookies=1548323620638',
        'Host':'fanyi.youdao.com',
        'Origin':'http://fanyi.youdao.com',
        'Referer':'http://fanyi.youdao.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
}

# 处理Form表单数据
data = {
        "i":key,
        "from":"AUTO",
        "to":"AUTO",
        "smartresult":"dict",
        "client":"fanyideskweb",
        "salt":str(salt),
        "sign":sign,
        "ts":str(ts),
        "bv":"363eb5a1de8cfbadd0cd78bd6bd43bee",
        "doctype":"json",
        "version":"2.1",
        "keyfrom":"fanyi.web",
        "action":"FY_BY_REALTIME",
        "typoResult":"false",
    }

res = requests.post(url,data=data,
                        headers=headers)
res.encoding = 'utf-8'
html = res.text

# loads()可把json格式的字符串转为Python
# 的数据类型
rDict = json.loads(html)
result = rDict['translateResult'][0][0]['tgt']
print(result)


#{"type":"ZH_CN2EN",
# "errorCode":0,
# "elapsedTime":0,
# "translateResult":
#   [[{"src":"老虎","tgt":"The tiger"}]]}












