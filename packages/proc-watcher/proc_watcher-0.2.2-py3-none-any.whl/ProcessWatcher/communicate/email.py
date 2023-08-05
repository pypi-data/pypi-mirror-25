import logging
import smtplib
from email.mime.text import MIMEText

from . import get_config_file

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def send(to=None, process=None, subject_format='{executable} process {pid} ended'):
    """Send email about the ended process.

    :param to: email addresses to send to
    :param process: information about process. (.info() inserted into body)
    :param subject_format: subject format string. (uses process.__dict__)
    """
    if to is None or len(to) < 1:
        raise ValueError('to keyword arg required')
    cp = configparser.ConfigParser()
    cp.read(get_config_file())
    mail_user = cp.get('email', 'user_email')
    mail_pass = cp.get('email', 'user_password')
    mail_server = cp.get('email', 'server')
    mail_server_port = cp.get('email', 'port')
    html = '''<html>
    <body>
    <content>{body}</content>
    <footer>(automatically sent by process-watcher program)</footer>
    </body>
    </html>'''.format(body='' if process is None else process.info())

    msg = MIMEText(html, 'html')
    msg['Subject'] = subject_format.format(**process.__dict__)
    # From is required
    msg['From'] = mail_user
    msg['To'] = to if type(to) is str else', '.join(to)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP(mail_server, port=mail_server_port, timeout=15)
    try:
        s.ehlo_or_helo_if_needed()
        s.starttls()
    except smtplib.SMTPNotSupportedError:
        pass
    try:
        s.login(mail_user, mail_pass)
    except smtplib.SMTPNotSupportedError:
        pass
    try:
        logging.info('Sending email to: {}'.format(msg['To']))
        s.send_message(msg)
    except Exception as e:
        logging.exception(e)
    finally:
        s.quit()
