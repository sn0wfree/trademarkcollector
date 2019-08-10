# coding=utf8


from collections import namedtuple

xpath_autosearch = {'国际分类': ('xpath', 'input', '//*[@id="nc"]'),
                    '类似群': ('css', 'condition-input', 'html body form#submitForm div.main_centent div.searchbox table tbody tr td div.inputbox input.input'),

                    '查询方式': ('xpath', 'point', '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/ul'),
                    '商标名称': ('xpath', 'input', '//*[@id="mn"]'),

                    '重填': ('css', 'bottom', 'html body form#submitForm div.main_centent div.bottonbox input.bottona'),
                    '查询': ('css', 'bottom',
                           'html body form#submitForm div.main_centent div.bottonbox input#_searchButton.bottona.bottonb')

                    }

xpath_selectsearch = {'国际分类': ('xpath', 'input', '//*[@id="nc"]'),
                      '类似群': ('xpath', 'condition-input', '//*[@id="queryType"]]'),

                      '查询方式': ('xpath', 'point', '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/ul'),
                      '商标名称': ('xpath', 'input', '//*[@id="mn"]'),

                      '重填': ('xpath', 'bottom', '/html/body/form/div/div[3]/input[1]'),
                      '查询': ('xpath', 'bottom', '//*[@id="_searchButton"]')

                      }


def click_some(brows, css):
    brows.find_element_by_css_selector(css).click()


def send_keys(brows, loc, key):
    if loc[0] == 'xpath':

        brows.find_element_by_xpath(loc[-1]).send_keys(key)
    elif loc[0] == 'css':
        brows.find_element_by_css_selector(loc[-1]).send_keys(key)
    else:
        raise ValueError('unknown loc:{}'.format(loc))


def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


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


def type_in_mark_name(brows, key='大发'):
    if is_all_chinese(key):
        pass
    else:
        raise ValueError('mark name must be all chinese string!')
    send_keys(brows, xpath_autosearch['商标名称'], key)


def click_search_botton_autosearch(brows, css=xpath_autosearch['查询'][-1]):
    click_some(brows, css)


def click_reset_botton_autosearch(brows, css=xpath_autosearch['重填'][-1]):
    click_some(brows, css)
