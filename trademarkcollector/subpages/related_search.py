# coding=utf8
import random
import time

from selenium.webdriver.common.action_chains import ActionChains

from trademarkcollector.paras.url import xpath_autosearch
from trademarkcollector.tools.check_chinese_string import is_all_chinese


def click_some(brows, css):
    brows.find_element_by_css_selector(css).click()


def send_keys(brows, loc, key):
    if loc[0] == 'xpath':
        item = brows.find_element_by_xpath(loc[-1])
        ActionChains(brows).move_to_element(item).click(item)

        brows.find_element_by_xpath(loc[-1]).send_keys(key)
    elif loc[0] == 'css':
        item = brows.find_element_by_css_selector(loc[-1])
        ActionChains(brows).move_to_element(item).click(item)
        brows.find_element_by_css_selector(loc[-1]).send_keys(key)
    else:
        raise ValueError('unknown loc:{}'.format(loc))


# def is_all_chinese(strs):
#     for _char in strs:
#         if not '\u4e00' <= _char <= '\u9fa5':
#             return False
#     return True


def type_in_nation_category(brows, key=9):
    if isinstance(key, int):
        pass
    else:
        raise ValueError('key must be int!')
    send_keys(brows, xpath_autosearch['国际分类'], key)


def type_in_related_group(brows, key=9):
    # if isinstance(key, int):
    #     pass
    # else:
    #     raise ValueError('key must be int!')
    send_keys(brows, xpath_autosearch['类似群'], key)


def type_in_mark_name(brows, keys='大发'):
    if is_all_chinese(keys):
        pass
    else:
        raise ValueError('mark name must be all chinese string!')

    for key in keys:
        time.sleep(random.random())
        send_keys(brows, xpath_autosearch['商标名称'], key)


def click_search_botton_autosearch(brows, css=xpath_autosearch['查询'][-1], retry=False):
    search_button = brows.find_element_by_css_selector(css)
    time.sleep(4)
    ActionChains(brows).move_to_element(search_button).click(search_button)
    click_some(brows, css)
    if retry:
        time.sleep(random.random() * 10)
        click_some(brows, css)


def click_reset_botton_autosearch(brows, css=xpath_autosearch['重填'][-1]):
    click_some(brows, css)


# ----------
css = "html.ng-scope body form#querylist.form-inline.ng-pristine.ng-valid div#mGrid_listGrid.ng-scope div#list_box.list_box table"

if __name__ == '__main__':
    import pickle

    file_ = "/Users/sn0wfree/PycharmProjects/trademarkcollector/trademarkcollector/test/related_search.text"
    with open(file_, 'rb') as f:
        s = pickle.load(f)

    pass
