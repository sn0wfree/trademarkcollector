# #coding=utf8
# import requests
#
#
# url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html'
#
# if __name__=='__main__':
#     url = "http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html"
#
#     headers = {
#         "Accept": "application/json, text/javascript, */*; q=0.01",
#         "Accept-Encoding": "gzip, deflate",
#         "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#         "Connection": "keep-alive",
#         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#         "Cookie": "",  # cookie
#         "Host": "sbgg.saic.gov.cn:9080",
#         "Origin": "http://sbgg.saic.gov.cn:9080",
#         "Referer": "http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=",
#         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
#         "X-Requested-With": "XMLHttpRequest",
#     }
#
#     data = {
#         "annNum": 12,
#         "annTypecode": 12,
#     }
#     response = requests.post(url=url, headers=headers, data=data, timeout=15)
#     id = response.text
#
# pass