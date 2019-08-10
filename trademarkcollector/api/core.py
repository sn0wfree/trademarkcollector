# coding=utf8
import time
from trademarkcollector.core.spider_body import Spider
from trademarkcollector.para.url import main_page_trademark_url
from trademarkcollector.core.preload_page import open_sbw_prefix_page
from trademarkcollector.core import proxy
from trademarkcollector.subpages.related_search import xpath_autosearch
from trademarkcollector.core.typein import type_and_click
from trademarkcollector.core.windowholder import WindowsHolder


class SBW(object):
    def __init__(self, web_address, headless=False):
        ip, port = proxy.get_proxy()
        print(ip, port)

        self.web_address = web_address

        self.spider = Spider(None, headless=headless, core='Firefox',
                             proxy='--proxy-server=http://{ip}:{port}'.format(ip=ip, port=port))

        self.windows = WindowsHolder(self.spider.driver)
        #

    def get_current_windows(self):
        return self.windows

    def checkip(self):
        return self.spider.driver.get("http://httpbin.org/ip")

    def preload(self):
        open_sbw_prefix_page(self.spider.driver, web_address=self.web_address, stop_time=3.5)
        # self.windows.add(name='main_pages')

    def main_goto(self, xpath):
        self.spider.driver.find_element_by_xpath(xpath).click()
        # self.windows.add(name='main_pages')

    def go_related_search(self):
        """
        商标近似查询
        :return:
        """
        self.main_goto('/html/body/div[3]/div[1]/ul/li[1]/table')
        self.windows.add(name='related_search')
        # self.spider.driver.find_element_by_xpath().click()

    def go_overall_search(self):
        """
        商标综合查询
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[2]/table'
        self.main_goto(xpath)
        self.windows.add(name='overall_search')

    def go_status_search(self):
        """
        商标状态查询
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[3]/table'
        self.main_goto(xpath)
        self.windows.add(name='status_search')

    def go_public_claim_search(self):
        """
        商标状态查询
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[4]/table'
        self.main_goto(xpath)
        self.windows.add(name='public_claim_search')

    def go_goods_service(self):
        """
        商品/服务项目
        :return:
        """
        xpath = '/html/body/div[3]/div[1]/ul/li[6]/table'
        self.main_goto(xpath)
        self.windows.add(name='goods_service')

#
# def get_new_pop_windows_handle_code(brows, exists_windows_list):
#     handle_windows_list = list(set(brows.window_handles) - set(exists_windows))
#     if len(handle_windows_list) == 1:
#         return handle_windows_list[0]
#     else:
#         raise ValueError('popup window own more than one window, please recheck!')

    #
    #     self.window_handle_code_holder[k] = v
    #
    # def


if __name__ == '__main__':
    web_address = 'http://sbj.cnipa.gov.cn/sbcx/'
    sbw = SBW(web_address)
    sbw.checkip()
    time.sleep(3)
    sbw.preload()
    time.sleep(3)
    sbw.go_related_search()


    # Container.window_handle_code_holder['main_window_handle'] = sbw.spider.driver.current_window_handle

    # main_window_handle = sbw.spider.driver.current_window_handle

    brows = sbw.spider.driver
    from trademarkcollector.subpages.related_search import *

    type_in_nation_category(brows, key=9)
    time.sleep(1)
    # type_in_related_group(brows, key='0901')
    # time.sleep(1)
    type_in_mark_name(brows, key='大发')
    time.sleep(1)

    click_search_botton_autosearch(brows)
    sbw.windows.add('result1')
    # Container.window_handle_code_holder['mark_search_result_window_handle_code'] = \
    #     list(set(brows.window_handles) - set([main_window_handle]))[0]
    # '42949967305'

    # single_result_pages_window_handle_code = \
    # list(set(brows.window_handles) - set([main_window_handle]) - set([mark_search_result_window_handle_code]))[0]
    #
    # brows.switch_to.window(single_result_pages_window_handle_code)

    pass
