import os
import sys
import subprocess32 as subprocess
import time

def generate_ssl(domain,custemail,country,id):
    try:
	timestr=time.strftime("%Y%m%d-%H%M%S")
        filename=str(id)+str(timestr)
	path=os.path.dirname(os.path.abspath(__file__))+"/"
        cmd="bash "+path+"scripts.sh "+domain+" "+custemail+" "+country+" "+path+filename
        t=subprocess.check_output(cmd,shell=True)
        return filename+".key.org"
    except Exception as e:
        return 0

if __name__=="__main__":
    print "sample paramerters"
    v=generate_ssl("a","b","c","d")
     
