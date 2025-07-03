import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()

class MailSender:

    def __init__(self):
        self.sender_mail = os.getenv("my_mail")
        self.password = os.getenv("password")

    def send_mail(self, mail, msg):
        try:
            email_msg = EmailMessage()
            email_msg['Subject'] = 'FLIGHT CLUB'
            email_msg['From'] = self.sender_mail
            email_msg['To'] = mail
            email_msg.set_content(msg)
            email_msg.set_charset('utf-8')  # Ensure it handles emojis and non-ASCII

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=self.sender_mail, password=self.password)
                connection.send_message(email_msg)
                print("Email sent successfully!")

        except Exception as e:
            print("Error sending email:", e)










