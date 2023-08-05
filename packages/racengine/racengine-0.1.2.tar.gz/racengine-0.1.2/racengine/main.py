from racengine.converter.converter import Converter
from racengine.email_sender.SMTPServer import SmtpServer
from racengine.exceptions import SMTPException, ConfigException
from racengine.templater.renderer import Renderer


class Process(object):
    def __init__(self, templater_endpoint=None, converter_endpoint=None, smtp_conf=None):
        self.__server = None
        if type(smtp_conf) is str:
            self.__server = SmtpServer(fileconf=smtp_conf)
        elif type(smtp_conf) is dict:
            self.__server = SmtpServer(
                smtp_conf.get('host', 'localhost'),
                int(smtp_conf.get('port', 465)),
                smtp_conf.get('username', ''),
                smtp_conf.get('password', '')
            )
        elif smtp_conf is not None:
            raise SMTPException('Invalid SMTP configuration type')

        if not (templater_endpoint or converter_endpoint):
            raise ConfigException('Need at least 1 endpoint, 0 given')

        self.__renderer = Renderer(templater_endpoint=templater_endpoint, smtp_server=self.__server)
        self.__converter = Converter(converter_endpoint=converter_endpoint, smtp_server=self.__server)

        self.__template = None
        self.__data = None
        self.__email_properties = None

    def set_template(self, file):
        self.__template = file

    def set_data(self, data):
        self.__data = data

    def set_msg(self, msg:dict):
        self.__email_properties = msg

    def run(self, output_format='pdf', flag='RCE'):
        result = False
        file = None

        # if flag:
        flags = set(flag)
        if flags - set("RCE") or len(flag) > len(flags):
            raise ValueError("invalid mode: %r" % flag)

        render = "R" in flags
        convert = "C" in flags
        send_email = "E" in flags
        if send_email and not(render or convert):
            raise ValueError("The E flag cannot be used alone")

        if render:
            result, file = self.render(
                                    self.__template,
                                    self.__data,
                                    self.__email_properties,
                                    not convert and send_email)

        if (result or not render) and convert:
            result, file = self.convert(file or self.__template, self.__email_properties, output_format, send_email)

            # return result, file

        # result, file = self.render(
        #                     self.__template,
        #                     self.__data,
        #                     self.__email_properties)
        # if result:
        #     result, file = self.convert(file, self.__email_properties, output_format, True)

        return result, file

    def render(self, template, data, email_properties=None, send_email=False):
        if template and data:
            return self.__renderer.run(template, data, email_properties, send_email)
        raise TypeError('Template file or/and Data is/are missing')

    def convert(self, file, email_properties=None, output_format="pdf", send_email=False):
        if file:
            return self.__converter.run(file, email_properties, output_format, send_email)
        raise TypeError('The file to convert is missing')