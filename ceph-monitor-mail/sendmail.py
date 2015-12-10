#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def smtp_conn(host, port, user, password):
    ''' smtp connection
        param host: str
        param port: int
        param user: str
        param password: str
        return: smtplib.SMTP instance
    '''
    try:
        session = smtplib.SMTP(host, port)
        print session.ehlo()
        print session.login(user, password)
        return session
    except smtplib.SMTPConnectError as msg:
        print msg
        print 'Connect to server Error, Please check host and port!'
        return False
    except smtplib.SMTPAuthenticationError as msg:
        print msg
        print 'Authentication Failure.  Please check username and password!'
        return False

def send_mail(session, mime, sender, recipient, subject, body):
    ''' use smtp send email
        param session: smtplib.SMTP instance
        param sender: unicode
        param recipient: unicode list
        param subject: unicode
        param body: unicode
        return: bool
    '''
    # Create the message ('plain' stands for Content-Type: text/plain)
    msg = MIMEMultipart('alternative')

    msg['From'] = sender
    msg['To'] = ','.join(recipient)
    msg['Subject'] =  Header(unicode(subject), 'utf-8')
    
    if mime == 'text':
        part1 = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
    elif mime == 'html':
        part1 = MIMEText(body.encode('utf-8'), 'html', 'utf-8')
    else:
        print 'mime not include or error'
        return False

    msg.attach(part1)
    #print msg.as_string()

    try:
        status = session.sendmail(sender, recipient, msg.as_string())
        if status:
            print '%s sendmail failed' % recipient
            return False
        else:
            print '%s sendmail success' % recipient
            return True
    except (smtplib.SMTPHeloError,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPSenderRefused,
            smtplib.SMTPDataError) as msg:
        print msg
        return False
