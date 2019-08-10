# coding=utf8


class WindowsHolder(object):
    def __init__(self, brows):
        self.brows = brows
        self.window_handle_code_holder = dict()
        self.exists = []

    @property
    def get_current_window(self):
        return self.brows.current_window_handle

    @property
    def window_handles(self):
        return self.brows.window_handles

    def add(self, name):
        if not self.exists:
            exists = set()
        else:
            exists = set(self.exists)
        new_pop = list(set(self.window_handles) - exists)
        if len(new_pop) == 1:
            self.window_handle_code_holder[name] = new_pop[0]
            self.exists.append(new_pop[0])
            # return new_pop[0]
        elif len(new_pop) == 0:
            print('this is no new window popup!')
        else:
            raise ValueError('popup window own more than one window, please re-check!')
