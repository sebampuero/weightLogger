import utils.constants as EmailConstants
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Emailer(object):

    @classmethod
    def __stablish_connection(cls):
        cls.server = smtplib.SMTP(EmailConstants.SERVER, EmailConstants.PORT)
        print("Stablishing connection to {0}".format(EmailConstants.SERVER))
        cls.server.ehlo()
        cls.server.starttls()
        cls.server.login(EmailConstants.FROM_EMAIL, EmailConstants.PASS)


    @classmethod
    def send_email(cls):
        cls.__stablish_connection()
        msg = MIMEMultipart("alternative")
        msg['From'] = EmailConstants.FROM_EMAIL
        msg['To'] = "sebastian.ampuerom@gmail.com"
        msg['Subject'] = "Weight log reminder"
        msg.attach(MIMEText('You have not logged today!!!', 'plain'))
        print("Sending reminder email to sebastian.ampuerom@gmail.com")
        cls.server.sendmail(EmailConstants.FROM_EMAIL,"sebastian.ampuerom@gmail.com",msg.as_string())
        cls.server.quit()

