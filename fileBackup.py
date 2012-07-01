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
""
]

#FTP Variables
ftpCheck = 0 # 1 is you want FTP enabled, 0 if you do not 
ftp_server = ""
ftp_username = ""
ftp_password = ""

#SFTP/SCP Variables
sftpCheck = 0
ssh_server = ""
ssh_username = ""
ssh_password = ""
ssh_path = "" # Where this is going on the server end

#DropBox Variables  
dbCheck = 1
dbPath = ""
dbUser = ""
dbPassword = "" #NOTE: Your password is stored in this app in clear text but sent over SSL. If you want to be prompted leave this empty (obviously wont work for automated backups)

#MySQL Variables
mysqlCheck = 0 # 1 if you want mysqldumps to be enabled, 0 if you do not
mysql_host = ""
mysql_user = ""
mysql_pass = ""
#Use all if you want every database. If not just seperate it with a comma
mysql_db = [
]


zipDelete = 1 # 1 if you want the zip file to be deleted. 0 is useful if you want local backups

######## You should not need to edit below this line ########

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
			distutils.dir_util.copy_tree(i,savePath2 + i)
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

print "And we're zipped!"

#FTP - Use the following style -- up(host,username,password,directory,file)
if ftpCheck == 1:
	transferProg.ftpup(ftp_server,ftp_username,ftp_password,savePath,archive)
	print "FTP has finished!"
#SFTP - DESTINATION MUST INCLUDE FILENAME

if sftpCheck == 1:
	transferProg.sftpup(ssh_server,ssh_username,ssh_password,savePath + archive,ssh_path + archive)

#Dropbox
if dbCheck == 1:
	if dbPassword == "":
		import getpass
		dbPassword = getpass.getpass("Please enter your password: ")
	if dbPath[-1] != "/":
	        dbPath = dbPath + "/"
	transferProg.dropbox(savePath + archive,dbPath,archive,dbUser,dbPassword)

#Remove stuff

shutil.rmtree(savePath2)
if zipDelete == 1:
        os.remove(savePath + archive)
