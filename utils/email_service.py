import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    # Configure your SMTP server here (e.g., Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("your_email@gmail.com", "your_password")
        smtp.send_message(msg)