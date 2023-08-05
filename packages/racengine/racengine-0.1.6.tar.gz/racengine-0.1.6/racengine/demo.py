import json
import sys
from racengine.main import Process

if __name__ == "__main__":
    file_path = sys.argv[1]
    json_path = sys.argv[2]
    endpoint = ""
    conv_endpoint = ""
    smtp_conf = "./conf.json"  # or dict {"host": "", "port": 465, "username": "", "password": ""}

    msg = {
        'to': "s.regragui@sfereno.com",
        'from': "azer@exemple.com",
        'subject': "testaze",
        'text_body': "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org",
        'html_body': """\
                            <html>
                              <head></head>
                              <body>
                                <p>Hi!<br>
                                   How are you?<br>
                                   Here is the <a href="https://www.python.org">link</a> you wanted.
                                </p>
                              </body>
                            </html>
                        """
    }

    gen_and_conv = Process(templater_endpoint=endpoint, converter_endpoint=conv_endpoint, smtp_conf=smtp_conf)

    gen_and_conv.set_msg(msg)

    with open(json_path, 'r', encoding='utf-8') as f:
        json_ = json.loads(json.dumps(f.read()))
        gen_and_conv.set_data(json_)

    with open(file_path, 'rb') as f:
        gen_and_conv.set_template(f.read())

    print(gen_and_conv.run(flags='RCE'))
    print('Finish')
