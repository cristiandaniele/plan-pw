"""
Created on Fri Nov 27 11:17:33 2020
@author: criss_94
"""
import sys
import getpass
import json
from random import SystemRandom
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pkcs7 import PKCS7Encoder
import os
import string
import subprocess
import time

class recordPassword:
  def __init__(self, tag, id,pw,iv):
    self.tag = tag
    self.id = id
    self.pw = pw
    self.iv=iv


def setMasterPw(data):
    with open("settings.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def read_pw_from_key(type):
    if(type==0):
        print("[INFO] Insert master password")
    if(type==1):
        print("[INFO] Insert ID service")
    if(type==2):
        print("[INFO] Insert PW service")
    if(type==3):
        print("[INFO] Repeat master password")
    rootpw = getpass.getpass()
    if(rootpw.__len__()<16 and (type==0 or type==3)):
        rootpw=rootpw.zfill(16)
    if(rootpw.__len__()>16 and (type==0 or type==3)):
        print("[ERROR] Password length cannot be more than 16 character")
        return -1
    return rootpw

def readFile(pathFile,mode):
    try:
        file=open(pathFile,mode)
        fileString=file.read()
        return fileString
    except:
        print("[ERROR]File does not exist")

def decrypt(pw,cipher,iv):
    aes_decryptor = AES.new(pw, AES.MODE_CBC, (iv))#tofix
    message=aes_decryptor.decrypt((cipher))
    return message.decode("utf-8")

def encrypt(pw,message,iv):

    aes_encryptor = AES.new(pw, AES.MODE_CBC, str.encode(iv))#tofix
    encoder = PKCS7Encoder()
    padded_message=encoder.encode(message)
    cipher = aes_encryptor.encrypt(str.encode(padded_message))
    return cipher

def printManual():
    print("usage: python3 planpw.py [options] <flags> \n\
        [options]:\n\
            -get [tag]                      : get the password saved with [value] tag\n\
            -set [tag]                      : add a new password with the tag [value]\n\
            -find [string]                  : show all the tags matching with [string]\n\
            -craft <flags>                  : craft a new password\n\
                <-s>            -> allow special characters\n\
                <-l> [lenght]   -> set password lenght\n\
            -del [tag]                      : delete an existing password\n\
            -h                              : show this manual")

def checkHash(pw,masterPwHashed):
    if(pw==masterPwHashed):
        return 1
    return 0

def hash(pw):
    hash = SHA256.new()
    hash.update(str.encode((pw)))
    return hash.digest()
    
#main()
cryptogen = SystemRandom()

with open("settings.json", "r") as jsonFile:
    data = json.load(jsonFile)

masterPw_json=(data["masterPassword"])
pathFile=data["pathFile"] 
programToUse=data["programToUse"] 
tmp_file_path=data["tmp_file_path"] 

#check if it's the first access
if(masterPw_json=="-1"):
    print("*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*")
    print("*-*-*-*-*-* FIRST ACCESS *-*-*-*-*-*")
    rootpw=read_pw_from_key(0)
    rootpw_1=read_pw_from_key(3)
    if(rootpw==rootpw_1):
        data["masterPassword"]=str(hash(rootpw))
        setMasterPw(data)
        print("[INFO] The passwords has been saved!")
        masterPw_json=str(hash(rootpw))
    else:
        print("[INFO] The passwords do not match!")
    print("*-*-*-*-* END CONFIGURATION *-*-*-*-*")
    print("*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*\n")

if (len(sys.argv)==1):
    printManual()
for i in range(0 ,len(sys.argv)):
    if((sys.argv)[i]=="-find"):

        

        fileString=readFile(pathFile,"rb")
        try:
            tag_to_search=sys.argv[i+1]
        except:
            print ("[ERROR]Missing tag to search")
            break
        tag_to_show=[]
        print("[INFO]Seeking tag: "+tag_to_search)
        for word in fileString.split(str.encode("---")):
            if (str.encode(tag_to_search) in word.split(str.encode(":::"))[0]):
                tag_to_show.append(word.split(str.encode(":::"))[0].decode("utf-8"))
        tag_to_show = list(dict.fromkeys(tag_to_show))
        for tag in tag_to_show:
            print ("[QUERY OUTPUT] "+tag)
    if((sys.argv)[i]=="-del"):
        try:
            tag_to_del=sys.argv[i+1]
        except:
            print("[ERROR]Missing tag to delete")
            break
        fileString=readFile(pathFile,"rb")
        index_tag_start=fileString.find(str.encode(tag_to_del))
        index_tag_end=fileString.find(str.encode("---"),index_tag_start)+2
        fileString = fileString[0: index_tag_start:] + fileString[index_tag_end + 1::]
        file.close()
        file=open(pathFile,"wb")
        file.write((fileString))
        file.close()
        print("[LOG]Tag "+tag_to_del+" deleted")
    if((sys.argv)[i]=="-get"):
            valid=True
            tagToSearch = (sys.argv)[i+1]
            rootpw=(read_pw_from_key(0))
            hashed_root_pw=hash(rootpw)
            if(str(hashed_root_pw)!=masterPw_json):
                print("[WARNING] It is not your usual password.")
            allPw=[]
            try:
                file=open(pathFile,"rb")
                fileString=file.read()
            except:
                print("[ERROR] File not present in "+pathFile)
                quit
            records=[]
            records=fileString.split(b'---')

            for line in records:
                if(line!=b''):
                    _lines = line.split(b':::')
                    tmp=recordPassword(_lines[0].decode("utf-8"),_lines[1] ,_lines[2],_lines[3])
                    allPw.append(tmp)
            found=0
            error=False
            recordsToSave=""
            for x in allPw:
                if(x.tag==(tagToSearch)):
                    found=1
                    try:
                        recordsToSave+="Id: "+decrypt(rootpw, x.id,x.iv)+"\n"
                        recordsToSave+="Pw: "+decrypt(rootpw, x.pw,x.iv)+"\n"
                    except:
                        print("[ERROR]The password is wrong")
                        found=0
                        error=True
                        break
            if (error):
                break
            if (found==0):  
                print("[ERROR] Tag does not exist")
            else:
                print("[LOG]Correct password, showing the information")
                f= open(tmp_file_path,"w+")
                f.write(recordsToSave)
                f.close()
                subprocess.call(['open', '-a', 'TextEdit', tmp_file_path])
                time.sleep(10)
                print("[INFO] Removing the file..")
                os.remove(tmp_file_path)
    if((sys.argv)[i]=="-set"):
        valid=True
        rootpw=(read_pw_from_key(0))
        hashed_root_pw=hash(rootpw)
        if(str(hashed_root_pw)!=masterPw_json):
            print("[WARNING] You are using a different password, continue? y/n")
            tmp=input()
            if(tmp=="n" or tmp == "N" or tmp =="No" or tmp =="no"):
                break
        tag=(sys.argv)[i+1]
        id_to_save=read_pw_from_key(1)
        pw_to_save=read_pw_from_key(2)
        #secure random numbers
        safe_random_index=[cryptogen.randrange(len(string.ascii_letters)) for i in range(16)]
        iv=''.join(string.ascii_letters[index] for index in safe_random_index)

        #not secure random numbers
        # iv=''.join(random.choice(string.ascii_letters) for x in range(16)) 
        with open(pathFile,"ab") as file_in:
            file_in.write(str.encode(tag))
            file_in.write((b":::"))
            file_in.write(encrypt(rootpw, id_to_save,iv))
            file_in.write((b":::"))
            file_in.write(encrypt(rootpw, pw_to_save,iv))
            file_in.write((b":::"))
            file_in.write(str.encode(iv))
            file_in.write((b"---"))
        print("[INFO] The password has been saved")
    if((sys.argv)[i]=="-craft"):
        length=15
        valid=True
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        alphabet_special="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_.:,;+*[]()/=\'|!?\"$%&/"
        alph=alphabet
        index=0
        for command in sys.argv:
            if (command=="-s"):
                alph=alphabet_special
            if (command=="-l"):
                length=int(sys.argv[index+1])
                print("[INFO]Set length password = "+str(length))
                if(length<8):
                    print("[WARNING]Weak password")
            index=index+1
        safe_random_index=[cryptogen.randrange(len(alph)) for i in range(length)] 
        newPw=''.join(alph[index] for index in safe_random_index)
        f= open(tmp_file_path,"w+")
        f.write(newPw)
        f.close()
        subprocess.call(['open', '-a', programToUse, tmp_file_path])
        time.sleep(10)
        print("[INFO] Removing the file..")
        os.remove(tmp_file_path)