from mitmproxy import http
import os
import time
def checkFileOrDirectoryExist(folder):
    if os.path.exists(folder):
        return True
    else:
        return False
def prepareEnvironment(folder):
    check_directory_exist = checkFileOrDirectoryExist(folder)
    if(check_directory_exist == False):
        os.mkdir(folder)
        print("Mkdir directory "+ folder +" success!")
    else:
        print("Mkdir directory "+ folder +" existed!")
byte_content = []
tester_name = "lam"
folder = "/root/metadata-gdpr-server-"+tester_name+"/bytes/"
prepareEnvironment(folder)
def writeByte(byte_string,byte_name):
   with open(byte_name, "wb") as binary_file:
      binary_file.write(byte_string)
      print("Save bytes file "+byte_name)
def request(flow: http.HTTPFlow) -> None:
  if (flow.request.method =="PUT") or (flow.request.method =="POST") :
      print("---------------------------------")
      print(flow)
      header = flow.request.headers
      print(header)
      content = flow.request.content
      print("=================================")
      byte_content.append(content)
      print(byte_content)
      print("Length of byte_content is: "+str(len(byte_content)))
      for i in range(len(byte_content)):
         writeByte(byte_content[i],"/root/metadata-gdpr-server-"+tester_name+"/bytes/bytefile_"+str(i))
         time.sleep(0.2)
         