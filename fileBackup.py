import os
import shutil
import distutils.dir_util
import time
import ftpprog

#File Variables
savePath = "/Users/ssimpson/backup/"
files = [
"/Users/ssimpson/RTM/",
"/Users/ssimpson/Public",
"/Users/ssimpson/Books/Cisco Books/IPV6/Cisco.Press.Global.IPv6.Strategies.pdf"
]

#FTP Variables
ftp_server = "thisisnotaserver.com"
ftp_username = "dir@thisisnotaserver.com"
ftp_password = "0wgzt8bTUGJ9"

######## You should'nt need to edit below this line ########


#Copy the files over	
for i in files:
	if os.path.isdir(i):
		if i.split("/"[0])[-1] == "":
			distutils.dir_util.copy_tree(i,savePath + i.split("/"[0])[-2])
		else:
			distutils.dir_util.copy_tree(i,savePath + i.split("/"[0])[-1])
	else:
		shutil.copy2(i,savePath)

#Dump the databases

print "Files backed up! Lets zip..."

#Make the Archive
shutil.make_archive(savePath + "backup-" + time.strftime("%m%d%y"),"zip","/Users/ssimpson/backup/")
print "And we're zipped! Onto the FTP portion of the tour..."

#FTP - Use the following style -- up(host,username,password,directory,file)
ftpprog.up(ftp_server,ftp_username,ftp_password,savePath,"backup-" + time.strftime("%m%d%y") +".zip")

print "FTP has finished!"