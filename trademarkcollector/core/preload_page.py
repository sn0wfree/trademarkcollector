# coding=utf8


web_address = 'http://sbj.cnipa.gov.cn/sbcx/'

import time
from selenium.webdriver.common.keys import Keys


def open_sbw_prefix_page(driver, web_address='http://sbj.cnipa.gov.cn/sbcx/', stop_time=3.5):
    driver.get(web_address)
    time.sleep(stop_time)
    # local agree bottom
    xpath = '/html/body/div/div[5]/div[1]/div[1]/div/p[4]/a'  # /tbody/tr/td[1]/div/p
    driver.find_element_by_xpath(xpath).click()


if __name__ == '__main__':
    from trademarkcollector.core.spider_body import Spider
    chromedriver_mac_path = '/Users/sn0wfree/PycharmProjects/trademarkcollector/trademarkcollector/drivers/chromedriver_mac'
    firefoxdriver_mac_path = '/Users/sn0wfree/PycharmProjects/trademarkcollector/trademarkcollector/drivers/geckodriver'

    spider = Spider(None, headless=False, core='Firefox')
    open_sbw_prefix_page(spider.driver)
    # web_address = 'http://sbj.cnipa.gov.cn/sbcx/'
    # spider.driver.get(web_address)
    # # 找到百度的输入框，并输入“selenium”
    # time.sleep(4.5)
    # print(1)
    # xpath = '/html/body/div/div[5]/div[1]/div[1]/div/p[4]/a'  # /tbody/tr/td[1]/div/p
    # spider.driver.find_element_by_xpath(xpath).click()
    # search_text_blank = spider.driver.find_element_by_id('kw')
    # search_text_blank.send_keys('商标网')
    # search_text_blank.send_keys(Keys.RETURN)

    time.sleep(1)
    # "goUrl('/txnS01.do')"
    # 近似搜索

    # /html/body/div[3]/div[1]/ul/li[1]/table

    # 点击搜索按钮
    # spider.driver.find_element_by_id('su').click()

    # 获取当前的URL的地址

    pass
