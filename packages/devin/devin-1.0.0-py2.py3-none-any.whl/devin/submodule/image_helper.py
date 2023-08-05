from cStringIO import StringIO
from system_helper import SystemHelper
from date_helper import DateHelper
from PIL import Image
import os


class ImageHelper(object):

    @staticmethod
    def show_image_from_web(img_url, user=None, password=None):
        if user is None or password is None:
            img_data = WebHelper.get_auth_web_source(img_url)
        else:
            img_data = WebHelper.get_auth_web_source(img_url, user, password)
        ImageHelper.show_image_from_data(img_data)

    @staticmethod
    def show_image_from_data(data):
        if os.name == 'posix':
            img = Image.open(StringIO(data))
            img.show()
        else:
            print "deprecated method for windows system!"
            tmp_file = 'tmp_%s.jpg' % DateHelper.get_current_timestamp()
            ImageHelper.save_image_file(data, tmp_file)
            ImageHelper.show_from_file(tmp_file)
            SystemHelper.delete(tmp_file)

    @staticmethod
    def show_from_file(local_image_file):
        if os.name == 'posix':
            os.system('open %s' % local_image_file)
        elif os.name == 'nt':
            os.system('start %s' % local_image_file)
        else:
            print "os type %s not support in ImageHelper!" % os.name
            os.system('start %s' % local_image_file)

    @staticmethod
    def save_image_file(image_data, local_file):
        opener = open(local_file, 'wb')
        opener.write(image_data)
        opener.close()

    @staticmethod
    def create_image_from_web(img_url, user=None, password=None):
        if user is None or password is None:
            img_data = WebHelper.get_web_source(img_url)
        else:
            img_data = WebHelper.get_auth_web_source(img_url, user, password)
        return Image.open(StringIO(img_data))