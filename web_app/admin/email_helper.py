import certifi
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# from config import EMAIL_ACCOUNT, EMAIL_PASSWORD, HOST, PORT
#
# # Create a secure SSL context
# context = ssl.create_default_context()
# context.load_verify_locations(certifi.where())
#
# message = MIMEMultipart("alternative")
# message["Subject"] = "multipart test"
# message["From"] = EMAIL_ACCOUNT
# message["To"] = "viktorsalimov544@gmail.com"
#
# text = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
# html = """\
# <html>
#   <body>
#     <p>Hi,<br>
#        How are you?<br>
#        <a href="http://www.realpython.com">Real Python</a>
#        has many great tutorials.
#     </p>
#   </body>
# </html>
# """
#
# # Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html, "html")
#
# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
# message.attach(part1)
# message.attach(part2)
#
# with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
#     server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
#     server.sendmail(EMAIL_ACCOUNT, "viktorsalimov544@gmail.com", message.as_string())
