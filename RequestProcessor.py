import re
import os
import sys
import os.path
from pathlib import Path

#test_regex = "^([^:\/\s\?]+ \/)?([^:\/\s\?]+)?"
test_regex = r"^([^:\/\s\?]+ \/)?([^:\/\s\?]+)?(.*\s.*)*(\s\s)(.*)?"


directory = "data"
verbose = False

def setDirectory(newDirectory):
    global directory
    directory = newDirectory
    print("Directory variable has been set to ", directory)

def setVerbose():
    global verbose
    verbose = True



def parse_request(request):
    global directory
    global verbose

    request = request.decode()
    if(verbose == True):
        print("Request", request)
    matcher = re.search(test_regex, request)
    request_type = matcher.group(1)


    if(request_type=='POST /'):
       # print("Request", request)
        # get file
        request_details = matcher.group(2)

        # get data
        request_data = matcher.group(3)
        my_file = Path("%s/%s.txt" % (directory, request_details))

        f = open(my_file, 'w')
        f.write(request_data)   
        return(request_data)         


    if(request_type =='GET /'):

        if(matcher.group(2)):
            request_details = matcher.group(2)
            print("Request Details", request_details)

            my_file = Path("data/%s.txt" % request_details)
            if os.path.isfile(my_file):
                f = open(my_file, 'r')
                file_contents = f.read()
                return (file_contents)
                
            else:
                error_message = "Error 404: File Not Found"
                return(error_message)


        else:
            return str(os.listdir(os.getcwd() + r'\data'))




        