#!/usr/bin/python
# -*- coding: utf-8 -*-


class ConfigHelper(object):
    @staticmethod
    def parse(config_file, sep='=', comment_char='#'):
        """
        Read the file passed as parameter as a properties file.
        """
        props = {}
        with open(config_file, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
        return props


if __name__ == '__main__':
    _test_file = '../configuration.properties'
    print (ConfigHelper.parse(_test_file)['DEVICE_TYPE'])
