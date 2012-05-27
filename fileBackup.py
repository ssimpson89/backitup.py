import os
import shutil
import distutils.dir_util
import time
import transferProg
import subprocess
import tarfile
import gzip


#File Variables
savePath = ""
files = [
]

#FTP Variables
ftpCheck = 0 # 1 is you want FTP enabled, 0 if you do not 
ftp_server = ""
ftp_username = ""
ftp_password = ""

#MySQL Variables
mysqlCheck = 1 # 1 if you want mysqldumps to be enabled, 0 if you do not
mysql_host = ""
mysql_user = ""
mysql_pass = ""
#Use all if you want every database. If not just seperate it with a comma
mysql_db = [
]

zipDelete = 0 # 1 if you want the zip file to be deleted. 0 is useful if you want local backups

######## You should not need to edit below this line ########

print savePath
if savePath[-1] != "/":
        savePath = savePath + "/"
savePath2 = savePath + "files/"
try:
	os.mkdir(savePath2)
except:
	pass	
#Copy the files over	
for i in files:
	try:
		if os.path.isdir(i):
	
			if i.split("/"[0])[-1] == "":
				distutils.dir_util.copy_tree(i,savePath2 + i.split("/"[0])[-2])
			else:
				distutils.dir_util.copy_tree(i,savePath2 + i.split("/"[0])[-1])
		else:
			shutil.copy2(i,savePath2)
	except:
		pass
#Dump the databases

if mysqlCheck == 1:
	os.mkdir(savePath2 + "sql/")
        for i in mysql_db:
                if i.lower() == "all":
                        subprocess.call("for i in $(echo 'show databases' | mysql) ; do $(mysqldump --user " + mysql_user + " --password=" + mysql_pass + " --force --flush-privileges $i  > " + savePath2 + "/sql/$i.sql); done", shell=True)
                else:
                        subprocess.call("mysqldump --user " + mysql_user + " --password=" + mysql_pass + " --force --flush-privileges " + i + "  > " + savePath2 + "sql/" + i + ".sql", shell=True)


print "Files backed up! Lets zip..."

#Make the Archive
archive = "backup-" + time.strftime("%m%d%y") + ".tar.gz"
tar = tarfile.open(savePath + archive,mode='w:gz')
tar.add(savePath2)
tar.close()

print "And we're zipped! Onto the FTP portion of the tour..."

#FTP - Use the following style -- up(host,username,password,directory,file)
if ftpCheck == 1:
	transferProg.ftpup(ftp_server,ftp_username,ftp_password,savePath,archive)
	print "FTP has finished!"

#Remove stuff

shutil.rmtree(savePath2)
if zipDelete == 1:
        os.remove(savePath + archive)
