"""File: bots/whatsapp.py"""
""" To send whatsapp message to users via web.whatsapp.com """

import pywhatkit

def sendMsg(reciever, content):
    reciever = f"+91{reciever}"

    # web.whatsapp.com will open in your default browser
    # the message will be sent to the given number after a few seconds
    # the browser tab will be closed then
    pywhatkit.sendwhatmsg_instantly(reciever, content, wait_time=20, tab_close=True, close_time=3)

if __name__ == '__main__':
    # sendMsg("", "hmmm")
    pass