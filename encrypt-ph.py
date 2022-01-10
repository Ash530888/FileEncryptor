import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import getpass

state=True
print("Welcome to the Python Cryptography program.\nThis program allows you to encrypt files and decrypt files.\n")

def nextStep():
    global state
    while state==True:
        choice=input("Would you like to 1)Continue using the program or 2)Exit: ")
        if choice=="1":
            Main()
        elif choice=="2":
            print("Goodbye!")
            state=False
        else:
            print("Invalid input! Valid inputs include '1' or '2'")


def encrypt(key, filename):
    chunksize=64*1024
    outputFile="(encrypted)"+filename
    filesize=str(os.path.getsize(filename)).zfill(16)
    IV=Random.new().read(16)

    encryptor=AES.new(key,AES.MODE_CBC,IV)

    with open(filename,'rb') as infile:
        with open(outputFile,'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk=infile.read(chunksize)
                if len(chunk)==0:
                    break
                elif len(chunk)%16!=0:
                    chunk+=b' '*(16-(len(chunk)%16))


                outfile.write(encryptor.encrypt(chunk))

    os.remove(filename)
    print("Done.\n")

    nextStep()

def decrypt(key, filename):
    chunksize=64*1024
    outputFile=filename[11:]

    with open(filename,'rb') as infile:
        filesize=int(infile.read(16))
        IV=infile.read(16)

        decryptor=AES.new(key, AES.MODE_CBC,IV)

        with open(outputFile,'wb') as outfile:
            while True:
                chunk=infile.read(chunksize)
                if len(chunk)==0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

    os.remove(filename)
    print("Done.\n")

    nextStep()
    
def getKey(password):
    hasher=SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def validPW(pw):
    global valid
    upper=0
    lower=0
    integer=0
    for i in pw:
        if i.isupper():
            upper+=1
        elif i.islower():
            lower+=1
        elif i.isdigit():
            integer+=1
        if upper>0 and lower>0 and integer>0 and len(pw)>=8:
            valid=True
        else:
            valid=False


def exist(f):
    from pathlib import Path
    global found
    found=Path(f).is_file()

def Main():
    choice=input("Would you like to (E)ncrypt or (D)ecrypt?: ")
    if choice.upper()=='E':
        while True:
            filename=input("File to encrypt: ")
            exist(filename)
            if found==True:
                print("File found\n")
                break
            else:
                print("Can't find file. Make sure that the file is in the same area as the program.\n")
        print("We recommend that you use a strong password.\nIn order for your password to be strong it must be at least eight characters long and contain a mixture of integers, upper letters and lower letters.")
        while True:
            password=getpass.getpass()
            validPW(password)
            if valid==True:
                print("Strong password")
                break
            else:
                print("Your password isn't strong enough!\nYour password must be at least eight characters long and contain a mixtuer of integers, upper letters and lower letters.")
        encrypt(getKey(password),filename)
    elif choice.upper()=='D':
        while True:
            filename=input("File to decrypt: ")
            exist(filename)
            if found==True:
                print("File found\n")
                break
            else:
                print("Can't find file. Make sure that the file is in the same area as the program.\n")
        print("!!!\nWARNING! If wrong password entered, the file will be lost.\n!!!\n")
        password=getpass.getpass()
        decrypt(getKey(password),filename)
    else:
        print("No option selected...\n")
        nextStep()

if __name__=='__main__':
    Main()


