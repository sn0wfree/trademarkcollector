# coding=utf8
import random
import time

import pandas as pd
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException,WebDriverException
from urllib3.exceptions import MaxRetryError
from trademarkcollector.core.preload_page import open_sbw_prefix_page
from trademarkcollector.core.proxy import get_proxy
from trademarkcollector.core.spider_body import Spider
from trademarkcollector.core.windowholder import WindowsHolder
from trademarkcollector.paras.errors import IPError, BlockedIPError, GatewayTimeoutError
from trademarkcollector.paras.public_stop_time import stop
from trademarkcollector.subpages.related_search import type_in_nation_category, type_in_mark_name, \
    click_search_botton_autosearch
from trademarkcollector.subpages.subpages_paras import main_nav_dict
from trademarkcollector.subpages.related_search import ParseRelatedGroup, parse_related_search_detail_pages_process, \
    parse_related_search_detail_pages_info
from trademarkcollector.tools.retry_it import retry


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

    def check_ip(self, checkip_address="http://httpbin.org/ip"):
        # try:
        #     print('ss')
        self.spider.driver.get(checkip_address)
        #     alert = self.spider.driver.switch_to.alert
        # # return alert
        # except NoAlertPresentException:
        #     pass
        # else:
        #     print(1)
        #
        # return

    def get_page_source(self):
        return self.spider.driver.page_source

    def check_block_ip_error_status(self):
        print('check ip')
        if '出错啦！' in self.spider.driver.page_source:
            raise BlockedIPError('get error, ip may be blocked!')
        else:
            pass

    def check_block_504_error_status(self):
        print('check ip')
        if '504' in self.spider.driver.page_source:
            raise BlockedIPError('get 504 error, may need refresh')
        else:
            pass

    def check_gateway_timeout_error_status(self):
        print('check ip')
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
        print('init browser')
        super(SBW, self).__init__(web_address=web_address, headless=headless, ip_port=ip_port, core=core)
        ip_status = self.check_ip()
        time.sleep(stop)
        print(ip_status)

    @check_status_decorator
    def preload(self):

        print('init preload')
        open_sbw_prefix_page(self.spider.driver, web_address=self.web_address, stop_time=3.5)
        time.sleep(stop)
        print('done')
        # self.windows.add(name='main_pages')

    @check_status_decorator
    def main_goto(self, xpath):
        self.spider.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)

        # self.windows.add(name='main_pages')

    @check_status_decorator
    def _go_general_func(self, name):
        print('go to {} page'.format(name))
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


def click_twice_click_search_botton_autosearch(sbw):
    print('click')

    try:
        click_some, brows, css = click_search_botton_autosearch(sbw.spider.driver, retry=True)
        time.sleep(1.2 + random.random() * 3)
        sbw.windows.add('result1')
        result1 = sbw.windows.window_handle_code_holder['result1']
        sbw.spider.driver.switch_to_window(result1)
        sbw.check_block_ip_error_status()
        sbw.check_gateway_timeout_error_status()
        # s = sbw.get_page_source()
        # time.sleep(10 + random.random())
        # search page table
        # df = parse_table(sbw.get_page_source())
    except (BlockedIPError, GatewayTimeoutError) as e:
        print('double click')
        related_search = sbw.windows.window_handle_code_holder['related_search']
        sbw.spider.driver.switch_to_window(related_search)
        time.sleep(1.2 + random.random() * 3)
        click_some(brows, css)
        # click_search_botton_autosearch(sbw.spider.driver, retry=False)
        result1 = sbw.windows.window_handle_code_holder['result1']
        sbw.spider.driver.switch_to_window(result1)
        sbw.check_block_ip_error_status()
        sbw.check_gateway_timeout_error_status()
    else:
        print("page opened, don't need double click")
        pass


class RelatedSearchProcess(object):
    def __init__(self, web_address, headless=False, ip_port=None, core='Firefox'):
        self.browser_params_dict = dict(web_address=web_address, headless=headless, ip_port=ip_port, core=core)
        self.browser = self.init_browser()
        try:
            self.browser.preload()
        except WebDriverException as e:
            print(e)
            self.reload_browser()

        self._retry = False
        pass

    def init_browser(self):
        browser = SBW(**self.browser_params_dict)
        return browser

    def reload_browser(self):
        self.browser = self.init_browser()  # SBW(**self.browser_params_dict)
        self.browser.preload()
        time.sleep(.1)

    def go_related_search(self, checkip=True):
        self.browser.go_related_search()
        if checkip:
            self.browser.check_block_ip_error_status()
            time.sleep(2 + random.random() * 3)
        return self

    def type_process_related_search(self, nation_category_key=9, mark_name_keys='大润发'):
        brows = self.browser.spider.driver
        type_in_nation_category(brows, key=nation_category_key)
        time.sleep(2 + random.random() * 3)
        type_in_mark_name(brows, keys=mark_name_keys)
        time.sleep(1.2 + random.random() * 3)
        click_search_botton_autosearch(brows, retry=False)
        click_twice_click_search_botton_autosearch(self.browser)
        # status = self.browser.check_block_ip_error_status()
        self.browser.check_block_ip_error_status()
        self.browser.check_gateway_timeout_error_status()
        # print('error: {}'.format(status))
        self.browser.windows.add('result1')

    def general_double_click(self, page1_code,  page2_name, func_click, *args, **kwargs):
        retry_status = True

        try:
            func_click(*args, **kwargs)
            time.sleep(1.5 + random.random())
            self.browser.windows.add(page2_name)
            result1 = self.browser.windows.window_handle_code_holder[page2_name]
            self.browser.spider.driver.switch_to_window(result1)
            # check ip
            self.browser.check_block_ip_error_status()
            self.browser.check_gateway_timeout_error_status()
            retry_status = False
        except (IPError, BlockedIPError, GatewayTimeoutError, NoSuchElementException) as e:
            self.browser.spider.driver.switch_to_window(page1_code)
            func_click(*args, **kwargs)
            time.sleep(1.2 + random.random() * 3)
            result1 = self.browser.windows.window_handle_code_holder[page2_name]
            self.browser.spider.driver.switch_to_window(result1)
            # check ip
            self.browser.check_block_ip_error_status()
            self.browser.check_gateway_timeout_error_status()
            retry_status = False

        except TimeoutException as e:

            # count -= 1
            self.browser.spider.driver.quit()
        finally:
            return retry_status

    def goto_related_page_and_type_in(self, checkip=True, nation_category_key=9, mark_name_keys='大润发'):
        retry_status = True
        if self._retry:
            self.reload_browser()
        try:
            self.go_related_search(checkip=checkip)
            self.type_process_related_search(nation_category_key=nation_category_key, mark_name_keys=mark_name_keys)
            self.browser.check_block_ip_error_status()
            self.browser.check_gateway_timeout_error_status()
            retry_status = False
        except (IPError, BlockedIPError, GatewayTimeoutError, NoSuchElementException,WebDriverException) as e:
            print(e)
            self._retry = True
            print('retry')
            self.browser.spider.driver.quit()

        except TimeoutException as e:
            print(e)
            self._retry = True
            print('retry')
            # count -= 1
            self.browser.spider.driver.quit()
        finally:
            return retry_status

    @staticmethod
    def parse_html_table_from_pandas(page_source):
        return pd.read_html(page_source)

    @staticmethod
    def parse_result_table(page_source):
        # try:
        s = pd.read_html(page_source, header=0)[0].drop('Unnamed: 0', axis=1)
        # except ValueError as e:
        #     if 'No tables found' in str(e):
        #         raise BlockedIPError('get error, ip may be invalid!')
        #     else:
        #         raise ValueError(e)
        # else:
        return s

    def parse_related_search_result_table(self):

        self.browser.check_block_ip_error_status()
        self.browser.check_gateway_timeout_error_status()
        # get source
        result1 = self.browser.windows.window_handle_code_holder['result1']
        # switch_to_window
        self.browser.spider.driver.switch_to_window(result1)
        # check ip

        get_page_source = self.browser.get_page_source()

        df = self.parse_result_table(get_page_source)
        return df

    def do_related_search(self, nation_category_key=9, mark_name_keys='大润发', count=5):
        print('begin run!')

        while count:
            print('last {} try !'.format(count))
            retry_status = self.goto_related_page_and_type_in(nation_category_key=nation_category_key,
                                                              mark_name_keys=mark_name_keys)
            if retry_status:
                count -= 1
            else:
                break
        else:
            print('result page load completed!')
            pass

    @staticmethod
    def parse_related_search_detail_pages(sbw, tbody_xpath='//*/table/tbody/tr[@class="ng-scope"]'):
        trademark_tests = sbw.spider.driver.find_elements_by_xpath(tbody_xpath)
        for trade_mark in trademark_tests:
            ordernum = trade_mark.text.split(' ')[0]
            trade_mark.find_element_by_xpath('//*/td[@class="lwtd0"]/a').click()  # click one item into next page
            time.sleep(1 + random.random())
            sbw.windows.add(name='detail_pages_info_handles_code')
            sbw.spider.driver.switch_to_window(sbw.spider.driver.window_handles[-1])
            time.sleep(8 + random.random())
            try:
                sbw.check_block_ip_error_status()
                sbw.check_gateway_timeout_error_status()
                sbw.check_block_504_error_status()
            except (IPError, BlockedIPError, GatewayTimeoutError, NoSuchElementException) as e:

                sbw.spider.driver.switch_to_window(sbw.windows.window_handle_code_holder['result1'])
                trade_mark.find_element_by_xpath('//*/td[@class="lwtd0"]/a').click()  # click one item into next page

                sbw.spider.driver.switch_to_window(sbw.windows.window_handle_code_holder['detail_pages_info_handles_code'])
                time.sleep(1 + random.random())
            else:
                pass
            #
            # parse related pages detail info
            related_pages_detail_info = sbw.get_page_source()
            # to process

            trademark_process_button = sbw.spider.driver.find_element_by_xpath(
                '//*[@id="txnDetail2"]').click()
            time.sleep(1.3 + random.random())
            trademark_process_source = sbw.get_page_source()
            yield ordernum, related_pages_detail_info, trademark_process_source

    @retry(ExceptionToCheck=Exception, tries=100)
    def related_search_process(self, nation_category_key=9, mark_name_keys='大润发', count=5):
        #
        self.do_related_search(nation_category_key=nation_category_key, mark_name_keys=mark_name_keys, count=count)

        time.sleep(1 + random.random())

        df = self.parse_related_search_result_table()

        for order, info, process in self.parse_related_search_detail_pages(self.browser,
                                                                           tbody_xpath='//*/table/tbody/tr[@class="ng-scope"]'):
            t1, t2, t3 = parse_related_search_detail_pages_info(info)
            process_df, identification_info = parse_related_search_detail_pages_process(process)
            yield df, order, t1, t2, t3, process_df, identification_info

        # trademark_tests = self.browser.spider.driver.find_elements_by_xpath('//*/table/tbody/tr[@class="ng-scope"]')


def parse_trade_mark_detail():
    pass


# @retry(Exception, tries=4, delay=3, backoff=2)
def do_one_search(web_address='http://sbj.cnipa.gov.cn/sbcx/', nation_category=9, mark_name='大润发'):
    print('begin run!')
    count = 5
    while count:
        print('first try!')
        try:

            sbw = SBW(web_address)

            sbw.preload()
            time.sleep(1)

            sbw.go_related_search()
            print('error:', sbw.check_block_ip_error_status())
            brows = sbw.spider.driver
            time.sleep(2 + random.random() * 3)
            type_in_nation_category(brows, key=nation_category)
            # print('error:', sbw.check_block_ip_error_status())
            time.sleep(2 + random.random() * 3)
            type_in_mark_name(brows, keys=mark_name)
            # print('error:', sbw.check_block_ip_error_status())

            time.sleep(1.2 + random.random() * 3)
            click_twice_click_search_botton_autosearch(sbw)
            # click_search_botton_autosearch(brows, retry=False)
            print('error:', sbw.check_block_ip_error_status())
            sbw.check_block_ip_error_status()
            sbw.check_gateway_timeout_error_status()
            # sbw.windows.add('result1')
            break
        except (IPError, BlockedIPError, GatewayTimeoutError, NoSuchElementException) as e:
            print('retry')
            count -= 1
            sbw.spider.driver.quit()
        except(TimeoutException, MaxRetryError) as e:
            print('retry')
            # count -= 1
            sbw.spider.driver.quit()

    return sbw


@retry(ExceptionToCheck=Exception, tries=100)
def overall_test(web_address='http://sbj.cnipa.gov.cn/sbcx/'):
    sbw = do_one_search(web_address=web_address)
    time.sleep(1 + random.random())
    # parse result pages
    df = RelatedSearchProcess.parse_related_search_result_table(sbw)

    trademark_tests = sbw.spider.driver.find_elements_by_xpath('//*/table/tbody/tr[@class="ng-scope"]')
    for trade_mark in trademark_tests:
        # co2 = sbw.windows.window_handle_code_holder['related_search']
        # sbw.spider.driver.switch_to_window(co2)
        # trade_mark = trademark_tests[0]
        ordernum = trade_mark.text.split(' ')[0]

        trade_mark.find_element_by_xpath('//*/td[@class="lwtd0"]/a').click()  # click one item into next page
        sbw.windows.add(name='detail_pages_info_handles_code')
        sbw.spider.driver.switch_to_window(sbw.spider.driver.window_handles[-1])
        time.sleep(10 + random.random())
        # parse related pages detail info
        source = sbw.get_page_source()
        # to process

        trademark_process_button = sbw.spider.driver.find_element_by_xpath(
            '//*[@id="txnDetail2"]').click()
        time.sleep(1.3 + random.random())
        trademark_process_source = sbw.get_page_source()

        t1, t2, t3 = parse_related_search_detail_pages_info(source)
        # source = sbw.get_page_source()
        #
        #
        # t1, t2, t3 = ParseRelatedGroup.parse_first_table(source)
        # ------------------
        # parse trademark process
        # // *[ @ id = "txnDetail2"]

        # trademark_process_source = sbw.get_page_source()
        #
        # # search_button = brows.find_element_by_css_selector(css)
        #
        # sss = pd.read_html(trademark_process_source)
        # cols = ['申请/注册号', '业务名称', '环节名称', '结论', '日期']
        # identification_info = sss[0].values.ravel()[0]
        # process_df = pd.concat(sss[1:])
        # process_df.columns = cols
        process_df, identification_info = parse_related_search_detail_pages_process(trademark_process_button)

        yield ordernum, df, t1, t2, t3, process_df, identification_info


if __name__ == '__main__':
    web_address = 'http://sbj.cnipa.gov.cn/sbcx/'
    # for s in overall_test():
    #     df, t1, t2, t3, process_df, identification_info = s  # .next()
    #     break
    RSP = RelatedSearchProcess(web_address, headless=False, ip_port=None, core='Firefox')
    for s in RSP.related_search_process(nation_category_key=9, mark_name_keys='大润发', count=5):
        print(s)
        break

    # ActionChains(sbw.spider.driver).move_to_element(trademark_process_button).click(trademark_process_button)
    # click_some(brows, css)

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
