#!/usr/bin/python
# -*- coding: utf-8 -*-
import time


class DateHelper(object):
    @staticmethod
    def get_current_date():
        return time.strftime('%Y_%m_%d')

    @staticmethod
    def get_current_timestamp():
        return str(int(time.time()))

if __name__ == '__main__':
    print (DateHelper.get_current_date())