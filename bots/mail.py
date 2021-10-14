from cfg import MAIL_ID, MAIL_PASSWORD
import smtplib

def sendMail(reciever, sub, content):
    #header
    message = f"""From: eXlygenze {MAIL_ID}
    To: {reciever}
    Subject: {sub}\n
    {content} """

    server = smtplib.SMTP("smtp.gmail.com" , 587)
    server.starttls()
    try:    
        server.login(MAIL_ID,MAIL_PASSWORD)
        print("Logged in...")
        server.sendmail(MAIL_ID,reciever,message)
        print("email has been send!")
    except smtplib.SMTPAuthenticationError:
        print("Unable to sign in!")
    