# Directory cleaner : schedule: delete any duplicate files : make a log of deleted file name in log folder : send that file to a particlar mail id in sepecific interval of time

import hashlib
from sys import *
import schedule
import os
import time
import urllib
import urllib.request
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import datetime

def is_connected():
    try:
        urllib.request.urlopen('https://www.google.com',timeout=1)
        return True
    except Exception as e:
        return False

def MailSender(filename,time):
    try:
        fromaddr = "vasave.parag1@gmail.com"
        toaddr ="vasave.parag1@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = """
        Hello %s,
        
        This is auto generated mail.
        Please find attached document which contains log of duplicate deleted files.
        Log file is created at %s

        Thanks & Regards,
        Parag Hemant Vasave
        """ %(toaddr,time)

        Subject="""
        Duplicate deleted file log generated at : %s
        """%(time)

        msg['Subject'] = Subject
        
        msg.attach(MIMEText(body,'plain'))
        
        attachment = open(filename,"rb")

        p = MIMEBase('application','octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition',"attachment;filename= %s" %filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddr,password="ftcovznqukgzgrkf")

        text = msg.as_string()

        s.sendmail(fromaddr,toaddr,text)

        s.quit()

        print("Log file successfully sent through mail.")

    except Exception as E:
        print("Unable to send mail.",E)


def Delete_Files(dict1):
    results = list(filter(lambda x : len(x)>1,dict1.values()))

    iCnt = 0
    if len(results)>0:
        for result  in results:
            for subresult in result:
                iCnt+=1
                if iCnt>=2:
                    os.remove(subresult)
            iCnt = 0
    
def Hash_File(path,blocksize=1024):
    fd = open(path,"rb")
    hasher = hashlib.md5()
    buffer = fd.read(blocksize)

    while(len(buffer)>0):
        hasher.update(buffer)
        buffer = fd.read(blocksize)
    fd.close()
    return hasher.hexdigest()


def Find_Duplicate(path):
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)
    exists = os.path.isdir(path)

    dups = {}

    if exists:
        for foldername, subfolder, filename in os.walk(path):
            for file in filename:
                path = os.path.join(foldername,file)
                Hash_Code = Hash_File(path)

                if Hash_Code in dups:
                    dups[Hash_Code].append(path)
                else:
                    dups[Hash_Code]=[path]
        
        File_Log(dups)
        Delete_Files(dups)
        
    else:
        print("Invalid path")
    

def File_Log(dict2):

    log_dir = "DuplicateFileLog"
    ListFile=list()

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    seperator = "-"*100
    log_path=os.path.join(log_dir,"Duplicate File %s.txt"%(datetime.datetime.now().strftime("%d-%m-%Y~%H_%M_%S")))
    f = open(log_path,"w")
    f.write(seperator+"\n")
    f.write("Duplicate deleted file log : "+time.ctime()+"\n")
    f.write(seperator+"\n")
    f.write("\n")

    results = list(filter(lambda x : len(x)>1,dict2.values()))

    if len(results)>0:

        for result in results:
            for subresult in result:
                ListFile.append(subresult)
    else:
        pass

    for filename in ListFile:
        f.write("%s\n"%filename)
    
    f.close()
    
    print("Log file successfully generated at location : %s"%(log_path))

    connected = is_connected()
    if connected:
        MailSender(log_path,time.ctime())


def main():
    print("--------Automation script to find duplicate files--------")
    print("Application name : ",argv[0])

    if(len(argv)!=2):
        print("Error : Invalid number of arguments")
        exit()

    if((argv[1]=="-u") or (argv[1]=="-U")):
        print("Usage: ApplicationName AbsolutePath_of_DirectoryExtension")
        exit()
    if((argv[1]=="-h") or (argv[1]=="-H")):
        print("Help:This script is used to traverse specific directory and deleteduplicate file comparing checksum.")
        exit()

    try:

        schedule.every(10).seconds.do(Find_Duplicate, path=argv[1])
        while(True):
            schedule.run_pending()
            time.sleep(1)
            
    except Exception as e:
        print("Error : ",e)

if __name__=="__main__":
    main()