# Alogorithm:
# 1. Analyse file extension.
# 2. Seperate the file extension from the file
# 3. Make a folder with the name of that extension and move that file in that folder.
# 4. if the folder name of that extension already exists, then simply move that file to that folder

from sys import *
import os
import shutil  

def Directory_Organiser(path):

    flag = os.path.isabs(path)
    if flag == False:
        path = os.path.abspath(path)

    exists = os.path.isdir(path)

    if exists:

        for foldername,subfolder,filename in os.walk(path):
            for file in filename:
                ext=os.path.splitext(file)
                destpath = os.path.join(path,ext[1])
                try:
                    os.mkdir(destpath)
                except Exception:
                    pass
                try:    
                    shutil.move(os.path.join(foldername,file),destpath)
                except Exception as e:
                    print("Error : ",e)
                    print("Source file path : ",os.path.join(foldername,file))
                    pass
                    # Note : if there is a duplicate file an error will be generated showing the file
                    #        name on screen. The files will not be moved as OS doesn't support files with 
                    #        same name in same folder. Please note this files are compared only through names,
                    #        the files content can be different.
        print("Operation completed")
                    
    else:
        print("Invalid path.")

def main():
    print("--------------------Python Automation----------------------")
    print("Application name : ",argv[0])
    print("-----------------------------------------------------------")

    if(len(argv)!=2):
        print("Insufficicent arguments")
        print("Use -h for help or -u for usage.")
        exit()
    
    if((argv[1]=="-h")or(argv[1]=="-H")):
        print("This application is use to organise the files as per there extensions.")
        exit()
    
    if((argv[1]=="-u")or(argv[1]=="-U")):
        print("Usage command : python Application_Name AbsolutePath_of_Directory")
        exit()
    
    try:
        Directory_Organiser(argv[1])
    
    except Exception as e:
        print("Error : ",e)

if __name__=="__main__":
    main()