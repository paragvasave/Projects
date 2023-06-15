# Note 1 : This application works for Gmail accounts. Please change the port number if you want to use another service provider.
# Note 2 : Two step verification must be on for gmail accounts and app password must be use for the below script.

from sys import *
import schedule
import os
import psutil
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
    except urllib.URLError as err:
        return False



def MailSender(filename,time):
    try:
        fromaddr = "Mail_address_of_sender"
        toaddr ="Mail_address_of_receiver"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = """
        Hello %s,
        
        This is auto generated mail.
        Please find attached document which contains Log of Running process.
        Log file is created at %s

        Thanks & Regards,
        Parag Hemant Vasave
        """ %(toaddr,time)

        Subject="""
        Process log generated at : %s
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

        s.login(fromaddr,password="-------")

        text = msg.as_string()

        s.sendmail(fromaddr,toaddr,text)

        s.quit()

        print("Log file successfully sent through mail.")

    except Exception as E:
        print("Unable to send mail.",E)



def ProcessLog(log_dir = "Process"):
    ListProcess=[]

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass
    
    seperator = "-"*80
    log_path = os.path.join(log_dir,"Process %s.txt"%(datetime.datetime.now().strftime("%d-%m-%Y~%H_%M_%S")))
    f = open(log_path,'w')
    f.write(seperator+"\n")
    f.write("Process Logger : "+time.ctime()+"\n")
    f.write(seperator +"\n")
    f.write("\n")

    for process in psutil.process_iter():
        try:
            processinfo = process.as_dict(['pid','username','name'])
            vms = process.memory_info().vms/(1024*1024)
            processinfo['vms']=vms
            ListProcess.append(processinfo)
        except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass
    
    for element in ListProcess:
        f.write("%s\n" %element)

    print("Log file is successfully generated at location %s" %(log_path))
    
    connected = is_connected()

    if connected:
        starTime = time.time()
        MailSender(log_path,time.ctime())



def main():
    print("-----------------Python Automation-----------------")
    print("Application Name : ",argv[0])

    if(len(argv)!=2):
        print("Error : Insufficient arguments")
        print("Use -h for help or -u for usage")
        exit()
    if((argv[1]=="-h")or(argv[1]=="-H")):
        print("Help - The script is use to log record of running process.")
        exit()
    
    if((argv[1]=="-u")or(argv[1]=="-U")):
        print("Usage : Application_Name Number_of_interval_in_Minutes")
        exit()

    try:
        schedule.every(int(argv[1])).minutes.do(ProcessLog)
        while(True):
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("Error : Invalid datatype of input")
    
    except Exception as E:
        print("Error: Invalid input",E)


if __name__=="__main__":
    main()