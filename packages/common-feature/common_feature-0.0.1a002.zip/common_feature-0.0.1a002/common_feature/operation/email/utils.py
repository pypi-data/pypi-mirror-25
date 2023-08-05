# -*- coding: utf-8 -*-
import requests


SPARKPOST_KEY = None
CONTACT_US_EMAIL = None


MAINGUN_KEY = None
DOMAIN_NAME = None


def normal_email(title, body, from_who, to_who):
    from django.core.mail import send_mail
    send_mail(title, body, from_email=from_who, recipient_list=to_who)


def sendmail_spark(subject, message, to=None, cc=None, bcc=None):
    if not SPARKPOST_KEY:
        return "Sparkpost Key is Needed"
    if not CONTACT_US_EMAIL:
        return "Contact us email is Needed"

    from sparkpost import SparkPost
    sp = SparkPost(SPARKPOST_KEY)
    if cc:
        cc = [cc]
    if bcc:
        bcc = [bcc]
    response = sp.transmissions.send(
        recipients=[to],
        html=message,
        from_email=CONTACT_US_EMAIL,
        subject=subject,
        cc=cc,
        bcc=bcc
    )


def sendmail_mailgun(subject, message, to=None, cc=None, bcc=None):
    if not MAINGUN_KEY:
        return "Mailgun key is needed"
    if not DOMAIN_NAME:
        return "Domain Name needed"

    if cc:
        cc = [cc]
    if bcc:
        bcc = [bcc]
    return requests.post(
        "https://api.mailgun.net/v3/"+DOMAIN_NAME+"/messages",
        auth=("api", MAINGUN_KEY),
        data={"from": CONTACT_US_EMAIL,
              "to": to,
              "cc": cc,
              "bcc": bcc,
              "subject": subject,
              "text": message,
              "html": "<html>HTML version of the body"+message+"</html>"}
    )