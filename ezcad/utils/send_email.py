# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import smtplib
from email.mime.text import MIMEText


def send_email(sender, receivers, subject, body, server='localhost'):
    """
    -i- sender : string, sender email address, format user@domain
    -i- receivers : list, strings of receivers' email addresses
    -i- subject : string, email subject line
    -i- body : string, email content
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)
    s = smtplib.SMTP(server) # port? work in Windows system?
    #s.send_message(msg) # work for single receiver
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()
    print("Successfully sent email")


def main():
    sender = 'zhu@company.com'
    receivers = ['zhu@company.com', 'xinfazhu@gmail.com']
    subject = 'This is subject'
    body = 'This is content'
    send_email(sender, receivers, subject, body)


if __name__ == '__main__':
    main()
