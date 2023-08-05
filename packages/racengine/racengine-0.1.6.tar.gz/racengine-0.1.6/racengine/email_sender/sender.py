import mimetypes
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from racengine.email_sender.SMTPServer import SMTPException


def prepare_and_send(email_properties, smtp_server):

    msg = MIMEMultipart()
    msg['Subject'] = email_properties.get('subject', '')
    msg['From'] = email_properties.get('from', None) or smtp_server.get('username', None)
    msg['To'] = email_properties.get('to')

    if email_properties.get('html_body', None):
        msg.attach(MIMEText(email_properties.pop('html_body'), 'html'))
        #msg.set_content(email_properties.pop('html_body'))

    if email_properties.get('html_text', None):
        msg.attach(MIMEText(email_properties.pop('html_text'), 'plain'))

    file = email_properties.get('file')
    file_format = email_properties.get('file_type')

    ctype = get_mimtype(file_format)
    maintype, subtype = ctype.split('/', 1)

    attach = MIMEApplication(file ,Name="rapport." + file_format)
    #attach.set_payload(base64.b64encode(file))
    # with open(file_path, 'rb') as fp:
    #     msg.get_payload()[1].add_related()
    #     attach = MIMEBase(maintype, subtype)
    #     attach.set_payload(fp.read())
    #encoders.encode_base64(attach)

    msg.add_header('Content-Disposition', 'attachment', filename="rapport." + file_format)

    msg.attach(attach)

    if not msg:
        raise SMTPException("Message missing")

    if not msg.get('To', None):
        raise SMTPException("Recipient(s) e-mail(s) missing")

    return smtp_server.send(msg)

def get_mimtype(file_type=None, file_path=None):
    mime_types = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
    if file_type:
        return mime_types.get(file_type, None)
    if file_path and type(file_path) is str:
        return mimetypes.guess_type(file_path)
    return None