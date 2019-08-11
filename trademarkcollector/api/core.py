# coding=utf8
import time

from selenium.common.exceptions import NoSuchElementException

from trademarkcollector.core.preload_page import open_sbw_prefix_page
from trademarkcollector.core.proxy import get_proxy
from trademarkcollector.core.spider_body import Spider
from trademarkcollector.core.windowholder import WindowsHolder
from trademarkcollector.paras.errors import IPError, BlockedIPError, GatewayTimeoutError
from trademarkcollector.paras.public_stop_time import stop
from trademarkcollector.subpages.subpages_paras import main_nav_dict


class PrepareSBW(object):
    def __init__(self, web_address, headless=False, ip_port=None, core='Firefox', ):
        if ip_port is None:
            ip, port = get_proxy()
        else:
            ip, port = ip_port
            print(ip, port)

        self.web_address = web_address

        self.spider = Spider(None, headless=headless, core=core,
                             proxy='--proxy-server=http://{ip}:{port}'.format(ip=ip, port=port))

        self.windows = WindowsHolder(self.spider.driver)

    def get_current_windows(self):
        return self.windows

    def check_ip(self):
        return self.spider.driver.get("http://httpbin.org/ip")

    def get_page_source(self):
        return self.spider.driver.page_source

    def check_block_ip_error_status(self):
        if '出错啦！' in self.spider.driver.page_source:
            raise BlockedIPError('get error, ip may be blocked!')
        else:
            pass

    def check_gateway_timeout_error_status(self):
        if 'ERROR: Gateway Timeout' in self.spider.driver.page_source:
            raise GatewayTimeoutError('get error, ip may be invalid!')
        else:
            pass


def check_status_decorator(func):
    def check(*args, **kwargs):
        args[0].check_block_ip_error_status()
        args[0].check_gateway_timeout_error_status()
        return func(*args, **kwargs)

    return check


class SBW(PrepareSBW):
    def __init__(self, web_address, headless=False, ip_port=None, core='Firefox', ):
        super(SBW, self).__init__(web_address=web_address, headless=headless, ip_port=ip_port, core=core)
        ip_status = self.check_ip()
        time.sleep(stop)
        print(ip_status)

    @check_status_decorator
    def preload(self):
        open_sbw_prefix_page(self.spider.driver, web_address=self.web_address, stop_time=3.5)
        time.sleep(stop)
        # self.windows.add(name='main_pages')

    @check_status_decorator
    def main_goto(self, xpath):
        self.spider.driver.find_element_by_xpath(xpath).click()

        # self.windows.add(name='main_pages')

    @check_status_decorator
    def _go_general_func(self, name):
        xpath = main_nav_dict[name]
        self.main_goto(xpath)
        self.windows.add(name=name)

    def go_related_search(self):
        """
        商标近似查询
        :return:
        """
        # self.main_goto('/html/body/div[3]/div[1]/ul/li[1]/table')
        # self.windows.add(name='related_search')
        self._go_general_func(name='related_search')
        # self.spider.driver.find_element_by_xpath().click()

    def go_overall_search(self):
        """
        商标综合查询
        :return:
        """
        # xpath = '/html/body/div[3]/div[1]/ul/li[2]/table'
        # self.main_goto(xpath)
        # self.windows.add(name='overall_search')
        self._go_general_func(name='overall_search')

    def go_status_search(self):
        """
        商标状态查询
        :return:
        """
        # xpath = '/html/body/div[3]/div[1]/ul/li[3]/table'
        # self.main_goto(xpath)
        # self.windows.add(name='status_search')
        self._go_general_func(name='status_search')

    def go_public_claim_search(self):
        """
        商标状态查询
        :return:
        """
        # xpath = '/html/body/div[3]/div[1]/ul/li[4]/table'
        # self.main_goto(xpath)
        # self.windows.add(name='public_claim_search')
        self._go_general_func(name='public_claim_search')

    def go_goods_service(self):
        """
        商品/服务项目
        :return:
        """
        # xpath = '/html/body/div[3]/div[1]/ul/li[6]/table'
        # self.main_goto(xpath)
        # self.windows.add(name='goods_service')
        self._go_general_func(name='goods_service')



# @retry(Exception, tries=4, delay=3, backoff=2)
def do_one_search(web_address='http://sbj.cnipa.gov.cn/sbcx/'):
    from trademarkcollector.subpages.related_search import type_in_nation_category, type_in_mark_name, \
        click_search_botton_autosearch
    count = 5
    while count:
        try:
            sbw = SBW(web_address)

            sbw.preload()
            time.sleep(3)
            sbw.go_related_search()
            print('error:', sbw.check_block_ip_error_status())
            brows = sbw.spider.driver
            time.sleep(1)
            type_in_nation_category(brows, key=9)
            print('error:', sbw.check_block_ip_error_status())
            time.sleep(1)
            type_in_mark_name(brows, keys='大润发')
            print('error:', sbw.check_block_ip_error_status())

            time.sleep(3)
            click_search_botton_autosearch(brows)
            print('error:', sbw.check_block_ip_error_status())
            sbw.windows.add('result1')
            break
        except (IPError, BlockedIPError, GatewayTimeoutError, NoSuchElementException) as e:
            print('retry')
            count -= 1
            sbw.spider.driver.quit()
    return sbw


def parse_table(page_source):
    import pandas as pd
    return pd.read_html(page_source, header=0)[0].drop('Unnamed: 0', axis=1)


if __name__ == '__main__':
    web_address = 'http://sbj.cnipa.gov.cn/sbcx/'

    sbw = do_one_search(web_address=web_address)

    sbw.spider.driver.switch_to_window(sbw.spider.driver.window_handles[-1])
    # s = sbw.get_page_source()
    time.sleep(10)
    df = parse_table(sbw.get_page_source())
    tests = sbw.spider.driver.find_elements_by_xpath('//*/table/tbody/tr[@class="ng-scope"]')
    test = tests[0]
    ordernum = test.text.split(' ')[0]

    test.find_element_by_xpath('//*/td[@class="lwtd0"]/a').click() # click one item into next page

    # import pickle
    #
    # with open('related_search.text', 'wb') as f:
    #     pickle.dump(s, f)

    # xpath = '/html/body/form/div/div[4]/table'
    # table = sbw.spider.driver.find_element_by_xpath(xpath)
    # sbw = SBW(web_address)
    # # sbw.check_ip()
    # sbw.preload()
    # time.sleep(3)
    # sbw.go_related_search()
    # print('error:', sbw.check_block_ip_error_status())

    # Container.window_handle_code_holder['main_window_handle'] = sbw.spider.driver.current_window_handle

    # main_window_handle = sbw.spider.driver.current_window_handle

    # brows = sbw.spider.driver
    # from trademarkcollector.subpages.related_search import *
    #
    # type_in_nation_category(brows, key=9)
    # print('error:', sbw.check_block_ip_error_status())
    # time.sleep(1)
    # type_in_related_group(brows, key='0901')
    # time.sleep(1)
    # type_in_mark_name(brows, key='大发')
    # print('error:', sbw.check_block_ip_error_status())
    # time.sleep(1)
    # time.sleep(1)
    # click_search_botton_autosearch(brows)
    # print('error:', sbw.check_block_ip_error_status())
    # sbw.windows.add('result1')
    # Container.window_handle_code_holder['mark_search_result_window_handle_code'] = \
    #     list(set(brows.window_handles) - set([main_window_handle]))[0]
    # '42949967305'

    # single_result_pages_window_handle_code = \
    # list(set(brows.window_handles) - set([main_window_handle]) - set([mark_search_result_window_handle_code]))[0]
    #
    # brows.switch_to.window(single_result_pages_window_handle_code)

    pass
