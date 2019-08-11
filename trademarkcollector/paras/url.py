# coding=utf8

main_page_trademark_url = "http://wsjs.saic.gov.cn/txnS01.do?dRmFctOl=qmMy1JLIrLgYH4Ct0G3KTiv7mSO4R14uZ1TTd9Qc7WzIK1NSkmz43GgcIsFjcgGvoBHOIDErS4k5SydeAEYhZkKVgkSH0lu16JVQBlnJvt68BbLooNKFt7.ulHsltsBfS5pUKu8lUcqrn6H.94ovPI8UR64JUa3KH1iERkYnsGlW1lki&zvgigpbz=2Wk2rCvgISoA45g1PdWtle2G78V16QHrjBybV6dl5PxyLFk7IqG27WvOhePoijkHXqFcFNAfRBW6CeYWWFDNrMREH.QqvO2Do9W2E7jsn3xPmzcF5zRIV4nx7GAr0jcIk"


xpath_autosearch = {'国际分类': ('xpath', 'input', '//*[@id="nc"]'),
                    '类似群': ('css', 'condition-input',
                            'html body form#submitForm div.main_centent div.searchbox table tbody tr td div.inputbox input.input'),

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