# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import


# 账户
class Account(object):

    def __init__(self, id, title, cash, positions):
        self.id = id
        self.title = title
        self.cash = cash
        self.positions = positions

    def match(self, title_or_id):
        if self.title == title_or_id:
            return True

        if self.id == title_or_id:
            return True