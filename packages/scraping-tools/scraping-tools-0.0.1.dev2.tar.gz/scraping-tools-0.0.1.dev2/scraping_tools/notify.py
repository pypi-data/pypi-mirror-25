import smtplib

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

from scraping_tools.logger import logger


def notify(sender_address,
           sender_password,
           message_subject,
           message_recipients,
           message_text_content,
           message_html_content):
    """Send an email to recipients.

    :param str sender_address: sender email address.
    :param str sender_password: sender email password.
    :param str message_subject: message subject.
    :param list message_recipients: recipients mail addresses
    :param str message_text_content: message body - textual format.
    :param unicode message_html_content: message body - HTML format.
    """
    logger.debug("Sending an email message %r to recipients %r", message_subject, message_recipients)
    message_recipients = ','.join(message_recipients)

    # Define a message object
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_address
    msg['To'] = message_recipients
    msg['Subject'] = message_subject

    msg.attach(MIMEText(message_text_content, 'plain'))
    msg.attach(MIMEText(message_html_content, 'html', _charset="UTF-8"))

    # Login to the SMTP server and send the message
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_address, sender_password)
    message_text_content = msg.as_string()
    server.sendmail(sender_address, message_recipients, message_text_content)
    server.quit()
