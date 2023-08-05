import json
import smtplib

from racengine.exceptions import SMTPException


class SmtpServer(object):
    def __init__(self, host='localhost', port=465, username='', password='', fileconf=None):
        conf = {}
        if fileconf:
            with open(fileconf, 'r') as f:
                conf = json.loads(f.read())
        self.host = conf.get('host', None) or host
        self.port = conf.get('port', None) or port
        self.username = conf.get('username', None) or username
        self.password = conf.get('password', None) or password
        self.server = smtplib.SMTP_SSL(host=self.host, port=self.port)

    def send(self, msg, emails=None, title='', subject='', attachment=''):
        # if emails is None and msg.get('To', None) is None:
        #     return False

        try:
            self.server.login(self.username, self.password)
        except (smtplib.SMTPHeloError,
                smtplib.SMTPNotSupportedError,
                smtplib.SMTPException):
            raise SMTPException('Error when tried to login')
        except smtplib.SMTPAuthenticationError:
            raise SMTPException('Invalid credentials')
        else:
            try:
                self.server.send_message(msg)
            except (smtplib.SMTPRecipientsRefused,
                    smtplib.SMTPSenderRefused,
                    smtplib.SMTPDataError):
                raise SMTPException('Error when sending e-mail')
            else:
                self.server.quit()
                return True