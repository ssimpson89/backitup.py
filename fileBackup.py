import os
import shutil
import distutils.dir_util
import time
import transferProg
import subprocess
import tarfile
import gzip


#File Variables
savePath = "/path/to/store/backup" #This is just the path where we want to temporarily store the files
files = [      #Add Files or Folders in quotes, 1 per line. Make sure the line ends with a comma
"/path/to/files",
]

#FTP Variables
ftpCheck = 0 # 1 is you want FTP enabled, 0 if you do not 
ftp_server = ""
ftp_username = ""
ftp_password = ""

#SFTP/SCP Variables
sftpCheck = 0 # 1 is you want sftp enabled
ssh_server = ""
ssh_username = ""
ssh_password = ""
ssh_path = "" # Where this is going on the server end

#DropBox Variables  
dbCheck = 0 # 1 is you want dropbox enabled
dbPath = ""
dbUser = ""
dbPassword = "" #NOTE: Your password is stored in this app in clear text but sent over SSL. If you want to be prompted leave this empty (obviously wont work for automated backups)

#s3 Variables
s3Check = 0
s3Bucket = ""
s3Key = ""
s3Secret = ""

#Google Drive
gdCheck = 0
gdUser = ""
gdPassword = "" #NOTE: Your password is stored in this app in clear text but sent over SSL. If you want to be prompted leave this empty (obviously wont work for automated backups)

#MySQL Variables
mysqlCheck = 0 # 1 if you want mysqldumps to be enabled, 0 if you do not
mysql_host = ""
mysql_user = ""
mysql_pass = ""
#Use all if you want every database in quotes. If not just seperate each line in quotes ending with a comma
mysql_db = [
]

tarZip = "zip" #Type 'zip' for zip and 'tar' to tar.gz
zipDelete = 0 # 1 if you want the zip file to be deleted. 0 is useful if you want local backups

######## You should not need to edit below this line ########

if savePath[-1] != "/":
        savePath = savePath + "/"
savePath2 = savePath + "files/"
try:
	os.mkdir(savePath2)
except:
	pass	
#Copy the files over
print("Backing up the files")
for i in files:
	try:
		if os.path.isdir(i):
			distutils.dir_util.copy_tree(i,savePath2 + i)
		else:
			shutil.copy2(i,savePath2)
	except:
		pass
		
#Dump the databases
print("Dumping the databases")
if mysqlCheck == 1:
	os.mkdir(savePath2 + "sql/")
        for i in mysql_db:
                if i.lower() == "all":
                        subprocess.call("for i in $(echo 'show databases' | mysql) ; do $(mysqldump --user " + mysql_user + " --password=" + mysql_pass + " --force --flush-privileges $i  > " + savePath2 + "/sql/$i.sql); done", shell=True)
                else:
                        subprocess.call("mysqldump --user " + mysql_user + " --password=" + mysql_pass + " --force --flush-privileges " + i + "  > " + savePath2 + "sql/" + i + ".sql", shell=True)


#Make the Archive
print("Creating the archive")
if tarZip == "tar":
	archive = "backup-" + time.strftime("%m%d%y") + ".tar.gz"
	tar = tarfile.open(savePath + archive,mode='w:gz')
	tar.add(savePath2)
	tar.close()
elif tarZip =="zip":
	try:
		import zipfile
	except:
		print("Please install zipfile")
	archive = "backup-" + time.strftime("%m%d%y") + ".zip"
	zip = zipfile.ZipFile(savePath + archive, 'w', zipfile.ZIP_DEFLATED)
	rootlen = len(savePath2) + 1
	for base, dirs, files in os.walk(savePath2):
		for file in files:
			fn = os.path.join(base, file)
			zip.write(fn, fn[rootlen:])


#FTP - Use the following style -- up(host,username,password,directory,file)
if ftpCheck == 1:
    print("Uploading to FTP")
	transferProg.ftpup(ftp_server,ftp_username,ftp_password,savePath,archive)
	print("FTP has finished!")

#SFTP - DESTINATION MUST INCLUDE FILENAME
if sftpCheck == 1:
    print("Uploading to SFTP")    
	transferProg.sftpup(ssh_server,ssh_username,ssh_password,savePath + archive,ssh_path + archive)
    print("SFTP Upload has finished")

#Dropbox
if dbCheck == 1:
	if dbPassword == "":
		import getpass
		dbPassword = getpass.getpass("Please enter your Dropbox password: ")
	if dbPath[-1] != "/":
	        dbPath = dbPath + "/"
    print("Uploading to dropbox")
	conn = transferProg.dbup(dbUser,dbPassword)
	conn.upload_file(savePath + archive,dbPath,archive)
	print("File uploaded as " + dbPath + archive)

#Amazon S3 
if s3Check == 1:
    print("Uploading to amazon")
	transferProg.s3up(s3Bucket,s3Key,s3Secret,archive,savePath) 
    print("Uploaded to amazon!")

#Google Drive
if gdCheck == 1:
	if gdPassword == "":
		import getpass
		gdPassword = getpass.getpass("Please enter your Google password: ")
    print("Uploading to Google Drive/Docs")
	transferProg.gdriveup(gdUser,gdPassword,archive,savePath + archive)
    print("Uploaded!")

#Remove stuff

shutil.rmtree(savePath2)
if zipDelete == 1:
    os.remove(savePath + archive)
    print("Zip file deleted")

print("And we're done!")