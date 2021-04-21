from time import *
import os


def email(
    sender_email=None, receiver_email=None, text=None, subject=None, password=None
):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    if sender_email != None:
        pass
    else:
        sender_email = input("Please put here your e-mail adress and press enter : ")
    if receiver_email != None:
        pass
    else:
        receiver_email = input(
            "Please put here the receiver e-mail adress and press enter : "
        )

    if password != None:
        pass
    else:
        password = input("Type your password and press enter :")

    message = MIMEMultipart("alternative")
    if subject != None:
        message["Subject"] = subject
    else:
        message["Subject"] = input("Put your e-mail subject and press enter : ")
    message["From"] = sender_email
    message["To"] = receiver_email
    if text != None:
        text = (
            """\
        """
            + text
        )
    else:
        text = """\
%s""" % input(
            "Tap your e-mail, then press enter : "
        )
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        "smtp." + sender_email[sender_email.index("@") + 1 :], 465, context=context
    ) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def emailTIME():
    temps = input("Envoyer le-mail tous les combien de temps  : ")
    email_sender = input("Your mail adress : ")
    email_receiver = input("The receiver mail adress : ")
    subject = input("Subject of your mail : ")
    text = input("Text of your mail : ")
    password = input("password : ")
    while True:
        email(email_sender, email_receiver, text, subject, password)
        sleep(int(temps))


email()
