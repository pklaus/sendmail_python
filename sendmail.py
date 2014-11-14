#!/usr/bin/env python

"""
Send an email. With Python.
"""

import smtplib
from email.mime.text import MIMEText
from email.charset import add_charset, QP
import argparse
import configparser

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--configfile', type=argparse.FileType('r'), required=True)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--from', required=True)
    parser.add_argument('--to', required=True)
    parser.add_argument('--configsection', default='DEFAULT')
    parser.add_argument('mailbody', metavar='MAILBODY', type=argparse.FileType('r'))
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.sections()
    config.read_file(args.configfile)
    print("Sections in the .ini file: {}".format(config.sections()))
    try:
        print("Values in the selected section '{}': {}".format(args.configsection, config.items(args.configsection)))
    except configparser.NoSectionError:
        print("Section {} not found.".format(args.configsection))

    add_charset('utf-8', QP, QP, 'utf-8')
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

