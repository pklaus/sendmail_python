#!/usr/bin/env python

"""
Send an email. With Python.
"""

import smtplib
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.charset import add_charset, QP
import os
import argparse
import configparser

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--from', required=True)
    parser.add_argument('--to', required=True)
    parser.add_argument('--configfile', type=argparse.FileType('r'), required=True, help='The .ini file with the mailserver credentials')
    parser.add_argument('--configsection', default='DEFAULT', help='The mail server section to choose in the configfile.')
    parser.add_argument('mailbody', metavar='MAILBODY', type=argparse.FileType('r'), help='A text file containing the mail body itself')
    parser.add_argument('attachments', metavar='ATTACHMENT', type=argparse.FileType('rb'), nargs='*', help='Optional files to attach')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.sections()
    config.read_file(args.configfile)
    try:
        args.configsection
        config.items(args.configsection)
    except configparser.NoSectionError:
        print("Section {} not found in configfile {}.".format(args.configsection, args.configfile.name))

    add_charset('utf-8', QP, QP, 'utf-8')
    if len(args.attachments):
        msg = MIMEMultipart()
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        mime_parts = []
        msg.attach(MIMEText(args.mailbody.read(), _charset='utf-8'))
        args.mailbody.close()
        for attachment in args.attachments:
            ctype, encoding = mimetypes.guess_type(attachment.name)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'image':
                mime_part = MIMEImage(attachment.read(), _subtype=subtype)
            else:
                mime_part = MIMEBase(maintype, subtype)
                mime_part.set_payload(attachment.read())
                encoders.encode_base64(mime_part)
            attachment.close()
            mime_part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment.name))
            msg.attach(mime_part)
    else:
        msg = MIMEText(args.mailbody.read(), _charset='utf-8')
        args.mailbody.close()
    
    msg['Subject'] = args.subject
    msg['From'] = getattr(args, 'from')
    msg['To'] = args.to

    server = smtplib.SMTP(config.get(args.configsection, 'server'), config.get(args.configsection, 'port'))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.get(args.configsection, 'username'), config.get(args.configsection, 'password'))

    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    main()

