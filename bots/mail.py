from cfg import MAIL_ID, MAIL_PASSWORD
import smtplib
sub="checking bot"
body= "hey everyone !!"
def sendMail(reciever, sub, body):
    #header
    message = 'Subject: {}\n\n{}'.format(sub,body)

    server = smtplib.SMTP("smtp.gmail.com" , 587)
    server.starttls()
    try:    
        server.login(MAIL_ID,MAIL_PASSWORD)
        print("Logged in...")
        server.sendmail(MAIL_ID,reciever,message)
        print("email has been send!")
    except smtplib.SMTPAuthenticationError:
        print("Unable to sign in!")
sendMail("karuna.sharma@iiitg.ac.in" , sub , body)