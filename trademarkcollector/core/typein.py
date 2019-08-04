# coding=utf8

#
# await page.type('input#kw.s_ipt','python')
# # 点击搜索按钮
# await page.click('input#su')

def type_func(brower_pypp, key_element_location, search_str):
    # 在搜索框中输入python
    brower_pypp.type(key_element_location, search_str)
    return brower_pypp


def click_search(brower_pypp, search_symbol):
    brower_pypp.click(search_symbol)
    return brower_pypp


def type_and_click(brower_pypp, key_element_location_dict, search_symbol):
    for loc, s_str in key_element_location_dict.items():
        brower_pypp.type(loc, s_str)
    brower_pypp.click(search_symbol)

    return brower_pypp


if __name__ == '__main__':
    pass
