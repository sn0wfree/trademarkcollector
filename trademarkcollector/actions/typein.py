# coding=utf8
import random
import time


def type_func(brower, key_element_location, search_str):
    # 在搜索框中输入python
    time.sleep(0.68 + random.random())
    brower.type(key_element_location, search_str)
    return brower


def click_search(brower, search_symbol):
    brower.click(search_symbol)
    return brower


def type_and_click(brower, key_element_location_dict, search_symbol):
    for loc, s_str in key_element_location_dict.items():
        # brower.type(loc, s_str)
        type_func(brower, loc, s_str)

    # brower.click(search_symbol)

    return click_search(brower, search_symbol)


if __name__ == '__main__':
    pass
