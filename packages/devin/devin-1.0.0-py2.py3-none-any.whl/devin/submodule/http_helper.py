#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests


class HttpHelper(object):
    @staticmethod
    def post(url, data_dict):
        print "Post with data ", data_dict
        response = requests.post(url, data=data_dict)
        return response.status_code, response.reason


if __name__ == '__main__':
    print HttpHelper.post('http://127.0.0.1:5000/api/v1/sensor/data', {"hello": "message"})