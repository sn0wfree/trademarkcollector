# -*- coding: utf-8 -*-
from selenium import webdriver

__author__ = 'sn0wfree'


class Spider(object):
    def __init__(self, driver_path, headless=True, core='Chrome', **other_kwargs):
        self.driver = SpiderSession.create_driver(driver_path, core=core, headless=headless, adaptive=False,
                                                  **other_kwargs)
        self.driver.implicitly_wait(10)
        pass


class SpiderSession(object):
    @staticmethod
    def _adaptive(driver, adaptive=True):
        if adaptive:
            driver.set_window_position(0, 0)
            driver.set_window_size(1024, 768)
        else:
            pass
        return driver

    @staticmethod
    def create_driver_Chrome(executable_path, headless=True, **other_kwargs):

        # .add_argument("--proxy-server=http://202.20.16.82:10152")
        option = webdriver.ChromeOptions()
        if other_kwargs is not None:
            for k, v in other_kwargs.items():
                print('add argument {}'.format(k))
                option.add_argument(v)

        if headless:
            option.add_argument('headless')
        pass

        driver = webdriver.Chrome(executable_path, chrome_options=option)
        # else:
        #     driver = webdriver.Chrome(executable_path)

        return driver

    @staticmethod
    def create_driver_Firefox(executable_path, headless=True, **other_kwargs):
        option = webdriver.FirefoxOptions()
        firefoxprofile = webdriver.FirefoxProfile()
        if other_kwargs is not None:

            for k, v in other_kwargs.items():
                print('add argument {}'.format(k))
                if k == 'proxy':

                    '--proxy-server=http://{ip}:{port}'
                    IP, PORT = v.split('--proxy-server=http://')[-1].split(':')

                    firefoxprofile.set_preference('network.proxy.type', 1)
                    firefoxprofile.set_preference('network.proxy.http', IP)  # IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
                    firefoxprofile.set_preference('network.proxy.http_port', int(PORT))  # PORT为代理服务器端口号:如，9999，整数类型
                    firefoxprofile.update_preferences()
                    # print(1)
                else:

                    option.add_argument(v)

        if headless:
            option.add_argument('headless')

        driver = webdriver.Firefox(executable_path="geckodriver", firefox_profile=firefoxprofile,
                                   firefox_options=option)
        # else:
        #     driver = webdriver.Firefox(executable_path)

        return driver

    @classmethod
    def create_driver(cls, executable_path, core='Chrome', headless=True, adaptive=True, **other_kwargs):
        if core == 'Chrome':
            driver = cls.create_driver_Chrome(executable_path, headless=headless, **other_kwargs)
            driver = cls._adaptive(driver, adaptive=adaptive)
        elif core == 'Firefox':
            driver = cls.create_driver_Firefox(executable_path, headless=headless, **other_kwargs)
            driver = cls._adaptive(driver, adaptive=adaptive)

        else:
            raise ValueError('unsupported driver!')
        return driver


if __name__ == '__main__':
    from trademarkcollector.core.proxy import get_proxy

    # SpiderSession.create_session(executable_path='tyc_finder/drivers/chromedriver_mac')
    # chromedriver_mac_path = '/Users/sn0wfree/PycharmProjects/trademarkcollector/trademarkcollector/drivers/chromedriver_mac'
    ip, port = get_proxy()

    spider = Spider(None, headless=False, core='Firefox',
                    proxy='--proxy-server=http://{ip}:{port}'.format(ip=ip, port=port))
    spider.driver.get("http://httpbin.org/ip")

    pass
