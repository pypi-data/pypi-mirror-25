#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import urllib2
from urlparse import urljoin
from urllib import urlretrieve
from urllib import quote_plus, unquote_plus
import cookielib
import requests
import re
from requests.auth import HTTPBasicAuth
from text_helper import TextHelper


class WebHelper(object):

    @staticmethod
    def get_cookie_content_from_url(web_url):
        req = urllib2.Request(web_url)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
        response = opener.open(req)
        data = response.read()
        cookie_list = []
        for cookie in cj:
            cookie_list.append(unquote_plus(cookie.value))
        return cookie_list, data

    @staticmethod
    def get_traverse_cookie(start_url, pre_pattern):
        cookies, web_source = WebHelper.get_cookie_content_from_url(start_url)
        if pre_pattern in web_source:
            next_para = web_source[web_source.index(pre_pattern) + len(pre_pattern):].strip()
            para_index = start_url.rindex('=') + len("=")
            next_url = start_url[:para_index] + next_para
            print("web source: " + web_source)
            print("Get next url: " + next_url)
            cookies.extend(WebHelper.get_traverse_cookie(next_url, pre_pattern))
        elif "Divide by two and keep going" in web_source:
            para_index = start_url.rindex('=') + len("=")
            para = start_url[para_index:]
            next_para = str(int(para) / 2)
            next_url = start_url[:para_index] + next_para
            print("web source: " + web_source)
            print("Get next url: " + next_url)
            cookies.extend(WebHelper.get_traverse_cookie(next_url, pre_pattern))
        return cookies

    @staticmethod
    def get_final_url_content(web_url, web_source=None):
        web_source = WebHelper.get_web_source(web_url) if web_source is None else web_source

        # If the web page is a plain text, if short enough, we can consider it is part of url promoted,
        # then we can join the origin url with these part promotion as the final url
        try:
            header = web_source[: web_source.index("/title")]
        except ValueError as TITLE_NOT_FOUND:
            print ("Not a well format web page")
            if len(web_source) < 15:
                print ("But a text prompt next url: " + web_source)
                final_url = urljoin(web_url, web_source)
                print ("Get final url: " + final_url)
                content = WebHelper.get_web_source(final_url)
                return final_url, content
            else:
                print ("Can not find prompt from url, return origin url")
                print (web_source)
                return web_url, web_source

        # If the page is html, and exist Redirection in header, then we find the promoted url and created the final url
        if "Redirection" in header:
            web_source = web_source[web_source.rindex("URL=") + len("URL="):]
            final_url = web_source[: web_source.index(".html") + len(".html")]
            final_url = urljoin(web_url, final_url)
            print ("Get final url: " + final_url)
            content = WebHelper.get_web_source(final_url)
            return final_url, content
        else:
            return web_url, web_source

    @staticmethod
    def get_web_source(url):
        response = urllib2.urlopen(url)
        web_source = response.read().strip()
        return web_source

    @staticmethod
    def get_auth_web_source(url, user='huge', password='file'):
        page = urllib2.HTTPPasswordMgrWithDefaultRealm()
        page.add_password(None, url, user, password)
        handler = urllib2.HTTPBasicAuthHandler(page)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        return urllib2.urlopen(url).read()

    @staticmethod
    def get_auth_web_source2(url, auth):
        response = requests.get(url, auth=auth)
        return response.content

    @staticmethod
    def join_url(origin_url, prompt):
        if "." not in prompt:
            suffix_index = origin_url.rindex(".")
            prompt += origin_url[suffix_index:]
        return urljoin(origin_url, prompt)

    @staticmethod
    def change_suffix_url(origin_url, suffix):
        suffix = suffix[1:] if "." in suffix else suffix
        suffix_index = origin_url.rindex(".") + len(".")
        return origin_url[:suffix_index] + suffix

    @staticmethod
    def get_traverse_url_content(start_url, pre_pattern):
        web_source = WebHelper.get_web_source(start_url)
        if pre_pattern in web_source:
            next_para = web_source[web_source.index(pre_pattern) + len(pre_pattern):].strip()
            para_index = start_url.rindex('=') + len("=")
            next_url = start_url[:para_index] + next_para
            print ("web source: " + web_source)
            print ("Get next url: " + next_url)
            return WebHelper.get_traverse_url_content(next_url, pre_pattern)
        elif "Divide by two and keep going" in web_source:
            para_index = start_url.rindex('=') + len("=")
            para = start_url[para_index:]
            next_para = str(int(para) / 2)
            next_url = start_url[:para_index] + next_para
            print ("web source: " + web_source)
            print ("Get next url: " + next_url)
            return WebHelper.get_traverse_url_content(next_url, pre_pattern)
        else:
            return start_url, web_source

    @staticmethod
    def download(web_url, store_path=None):
        store_path = WebHelper.get_url_page(web_url) if store_path is None else store_path
        urlretrieve(web_url, store_path)

    @staticmethod
    def download_with_auth(web_url, store_path=None, user_name='huge', pass_word='file'):
        response = requests.get(web_url, auth=HTTPBasicAuth(user_name, pass_word))
        store_path = WebHelper.get_url_page(web_url) if store_path is None else store_path
        print ("download file store into " + store_path)
        img = open(store_path, 'wb')
        img.write(response.content)

    @staticmethod
    def get_url_page(web_url):
        return web_url[web_url.rindex("/") + 1:]

    @staticmethod
    def get_auth_url_content(url, user='huge', password='file'):
        page = urllib2.HTTPPasswordMgrWithDefaultRealm()
        page.add_password(None, url, user, password)
        handler = urllib2.HTTPBasicAuthHandler(page)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        return response.geturl(), response.read()

    @staticmethod
    def get_prompt_url_from_web(url, start_tag, end_tag, user='huge', password='file'):
        url_ignore, web_content = WebHelper.get_auth_url_content(url, user, password)
        prompt_url_short = TextHelper.find_text_between_tag(web_content, start_tag, end_tag)
        prompt_url = WebHelper.join_url(url, prompt_url_short)
        print ("get new prompt url: %s" % prompt_url)
        return prompt_url

    @staticmethod
    def url_add(web_url):
        print ("Add 1 to url: %s" % web_url)
        page = WebHelper.get_url_page(web_url)
        (prefix, num, suffix) = re.search('(\w+[a-zA-Z])([0-9]+)(\.\w+)', page).groups()
        new_url = WebHelper.join_url(web_url, prefix + str(int(num) + 1) + suffix)
        print ("Get: %s" % new_url)
        return new_url


if __name__ == '__main__':
    # print WebHelper.get_traverse_url_content("http://www.pythonchallenge.com/pc/def/274877906944.html")
    # WebHelper.download_with_auth('http://www.pythonchallenge.com/pc/return/cave.jpg')
    WebHelper.url_add("some/w4u2.jo")