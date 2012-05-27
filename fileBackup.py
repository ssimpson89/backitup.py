import os
import shutil
import distutils.dir_util
import time
import transferProg

#File Variables
savePath = "/path/to/backup/"
files = [
"/path/to/files"
]

#FTP Variables
ftp_server = ""
ftp_username = ""
ftp_password = ""

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
shutil.make_archive(savePath + "backup-" + time.strftime("%m%d%y"),"zip",savePath)
print "And we're zipped! Onto the FTP portion of the tour..."

#FTP - Use the following style -- up(host,username,password,directory,file)
transferProg.ftpup(ftp_server,ftp_username,ftp_password,savePath,"backup-" + time.strftime("%m%d%y") +".zip")

print "FTP has finished!"