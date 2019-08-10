# coding=utf8
import time
from trademarkcollector.core.spider_body import Spider
from trademarkcollector.para.url import main_page_trademark_url
from trademarkcollector.core.preload_page import open_sbw_prefix_page
from trademarkcollector.core import proxy
from trademarkcollector.subpages.related_search import xpath_autosearch
from trademarkcollector.core.typein import type_and_click


class SBW(object):
    def __init__(self, web_address, headless=False):
        ip, port = proxy.get_proxy()
        print(ip, port)

        self.web_address = web_address

        self.spider = Spider(None, headless=headless, core='Firefox',
                             proxy='--proxy-server=http://{ip}:{port}'.format(ip=ip, port=port))
        #

    def checkip(self):
        return self.spider.driver.get("http://httpbin.org/ip")

    def preload(self):
        open_sbw_prefix_page(self.spider.driver, web_address=self.web_address, stop_time=3.5)

    def main_goto(self, xpath):
        self.spider.driver.find_element_by_xpath(xpath).click()

    def go_related_search(self):
        """
        商标近似查询
        :return:
        """
        self.main_goto('/html/body/div[3]/div[1]/ul/li[1]/table')
        # self.spider.driver.find_element_by_xpath().click()

    def go_overall_search(self):
        """
        商标综合查询
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[2]/table'
        self.main_goto(xpath)

    def go_status_search(self):
        """
        商标状态查询
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[3]/table'
        self.main_goto(xpath)

    def go_public_claim_search(self):
        """
        商标状态查询
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[4]/table'
        self.main_goto(xpath)

    def go_goods_service(self):
        """
        商品/服务项目
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[6]/table'
        self.main_goto(xpath)


if __name__ == '__main__':
    web_address = 'http://sbj.cnipa.gov.cn/sbcx/'
    sbw = SBW(web_address)
    sbw.checkip()
    time.sleep(3)
    sbw.preload()
    time.sleep(3)
    sbw.go_related_search()

    brows = sbw.spider.driver
    from trademarkcollector.subpages.related_search import *

    type_in_nation_category(brows, key=9)
    time.sleep(1)
    # type_in_related_group(brows, key='0901')
    time.sleep(1)
    type_in_mark_name(brows, key='大发')


    pass
