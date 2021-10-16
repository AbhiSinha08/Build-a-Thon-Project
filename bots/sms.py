import pywhatkit

def sendMsg(reciever, content):
    reciever = f"+91{reciever}"
    pywhatkit.sendwhatmsg_instantly(reciever, content, wait_time=20, tab_close=True, close_time=3)

if __name__ == '__main__':
    sendMsg("9016068450", "hmmm")