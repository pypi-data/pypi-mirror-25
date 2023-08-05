from racengine.converter.converter import Converter
from racengine.email_sender.SMTPServer import SmtpServer
from racengine.exceptions import SMTPException, ConfigException
from racengine.templater.renderer import Renderer

RENDER_FLAG = 'R'
CONVERT_FLAG = 'C'
SEND_EMAIL_FLAG = 'E'

ALL_FLAGS = 'RCE'


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

        self.__email_properties = None

    def run(self, output_format='pdf', flags=ALL_FLAGS, **kwargs):
        result = False
        file = None

        flags = set(flags)
        if flags - set(ALL_FLAGS):
            raise ValueError("invalid mode: %r" % flags)

        render = RENDER_FLAG in flags
        convert = CONVERT_FLAG in flags
        send_email = SEND_EMAIL_FLAG in flags

        if send_email and not(render or convert):
            raise ValueError("The E flag cannot be used alone")

        if render:
            assert "template" in kwargs, "Template file is missing"
            assert "data" in kwargs, "JSON data are missing"
            result, file = self.__render(
                                    kwargs.get("template"),
                                    kwargs.get("data"),
                                    self.__email_properties,
                                    not convert and send_email)

        if (result or not render) and convert:
            assert "file_to_convert" in kwargs or render, "File to convert is missing"
            result, file = self.__convert(
                file or kwargs.get("file_to_convert"),
                self.__email_properties,
                output_format,
                send_email
            )

        return result, file

    def __render(self, template, data, email_properties=None, send_email=False):
        if template and data:
            return self.__renderer.run(template, data, email_properties, send_email)
        raise TypeError('Template file or/and Data is/are missing')

    def __convert(self, file, email_properties=None, output_format="pdf", send_email=False):
        if file:
            return self.__converter.run(file, email_properties, output_format, send_email)
        raise TypeError('The file to convert is missing')