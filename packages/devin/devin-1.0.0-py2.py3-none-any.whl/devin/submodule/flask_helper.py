from bib_reader import BibReader
from system_helper import SystemHelper
from http_helper import HttpHelper
import time
import os
import json


class FlaskHelper(object):
    @staticmethod
    def start_read_service(data_directory, data_store_file, device_type, read_frequency=15, server_url=None):
        # step 1, parameters check
        status, error = FlaskHelper.parameter_check(data_directory, data_store_file, device_type, server_url)
        if status is False:
            print ("BIB read server start failed, failed reason: %s" % error)
            return
        # step 2, start server
        reader = BibReader(data_directory)
        print ("Start service reading bib device records!")
        while True:
            new_data = reader.read_new_data()
            print ("\nREADING....NEW...DATA")
            print (os.linesep.join(new_data))
            print ("Finished reading!\n")
            SystemHelper.append_to_file(data_store_file, os.linesep.join(new_data))

            # send data to server back-end
            send_data = {'deviceType': device_type, 'dataBatch': new_data}
            if server_url is not None and len(new_data) > 0:
                HttpHelper.post(server_url, send_data)
            time.sleep(read_frequency)

    @staticmethod
    def parameter_check(data_directory, data_store_file, device_type, server_url):
        if data_directory is None or len(data_directory) == 0:
            return False, "data directory is not configured"
        if data_store_file is None or len(data_store_file) == 0:
            return False, "data store file is not configured"
        if device_type is None or len(device_type) == 0:
            return False, "device type is not configured"
        if server_url is None or len(server_url) == 0:
            return False, "server url is not configured"
        return True, None