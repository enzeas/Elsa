#/usr/bin/env python3
# -*- coding: utf-8 -*-


class Cookie(object):
    def __init__(self, string):
        self._str = string
        self._cookie = self.parse_cookie()

    def parse_cookie(self):
        cookie_dict = {}
        items = self._str.split('; ')
        for item in items:
            arr = item.split('=')
            if len(arr) != 2:
                continue
            key, value = arr
            cookie_dict[key] = value
        return cookie_dict

    def cookie(self):
        return self._cookie


if __name__ == '__main__':
    c = Cookie(open('cookie.cfg').read())
    print(c.cookie())
