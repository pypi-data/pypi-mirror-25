#!/usr/bin/python
# -*- coding: utf-8 -*-
from email import Message, parser
import smtplib
import poplib

# Default configure
default_server = '163.com'
default_user = 'paypalshanghai@163.com'
default_password = 'mail163'


class EmailServer(object):
    def __init__(self, server_name=default_server, port=25):
        self.server_name = server_name
        self.smtp_server = 'smtp.%s' % server_name
        self.pop_server = 'pop.%s' % server_name
        self.port = port

    def __repr__(self):
        return "[Server Name:%s, SMTP Server:%s, POP Server:%s, Port:%d]" % (self.server_name, self.smtp_server,
                                                                             self.pop_server, self.port)


class UserConfig(object):
    def __init__(self, user_name=default_user, password=default_password):
        self.user_account = user_name
        self.password = password

    def __repr__(self):
        return "[User Name:%s, Password:%s]" % (self.user_account, self.password)


class EmailConfig(object):
    def __init__(self, email_server=EmailServer(), user_config=UserConfig()):
        self.email_server = email_server
        self.user_config = user_config

    def __repr__(self):
        return 'Email Server:%s, User Config:%s' % (self.email_server, self.user_config)


class Email(object):
    def __init__(self, from_, to_, subject, body):
        self.from_ = from_ if from_ is not None else 'paypalshanghai@163.com'
        self.to_ = to_
        self.subject = subject
        self.body = body

default_email_config = EmailConfig()


class EmailHelper(object):

    @staticmethod
    def send_mail(email_, email_config_=None):
        email_config = default_email_config if email_config_ is None else email_config_
        handle = smtplib.SMTP(email_config.email_server.smtp_server, email_config.email_server.port)
        handle.login(email_config.user_config.user_account, email_config.user_config.password)
        handle.sendmail(email_.from_, email_.to_, EmailHelper.build_email_msg(email_))
        handle.close()

    @staticmethod
    def build_email_msg(email_):
        email_message = Message.Message()
        email_message.add_header('To', email_.to_)
        email_message.add_header('From', email_.from_)
        email_message.add_header('Subject', email_.subject)
        email_message.set_payload(email_.body)
        return email_message.as_string()

    @staticmethod
    def get_latest_email(sender=None, email_config_=None):
        print "Starting to fetch the latest email!"
        email_config = default_email_config if email_config_ is None else email_config_
        handler = poplib.POP3(email_config.email_server.pop_server, timeout=10)
        handler.user(email_config.user_config.user_account)
        handler.pass_(email_config.user_config.password)
        count, size = handler.stat()
        print 'Response from server: Email total count %s, total size %s\n' % (count, size)
        if count == 0:
            print "No mail in mail box!"
            return None
        if sender is None:
            return parser.Parser().parsestr('\n'.join(handler.retr(count)[1]))
        # At most search in last ten email
        end = count - 10 if count > 10 else 1
        for i in range(count, end, -1):
            mail_tmp = parser.Parser().parsestr('\n'.join(handler.retr(i)[1]))
            if sender in mail_tmp['From']:
                return mail_tmp


if __name__ == '__main__':
    my_email = Email(default_user, 'leopold.moz@pythonchallenge.com', 'Apology', 'Sorry!')
    EmailHelper.send_mail(my_email)

    latest_mail = EmailHelper.get_latest_email('leopold.moz@pythonchallenge.com')
    if latest_mail is not None:
        print "sender: %s" % latest_mail['From']
        print "Receiver: %s" % latest_mail['To']
        print "Subject: %s" % latest_mail['Subject']
        print "Content: %s" % latest_mail.get_payload()