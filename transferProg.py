import ftplib
import os
import sys
try:	
	import paramiko
except:
	print("Paramiko is not installed. Visit lag.net/paramiko")
	
def ftpup(host,username,password,directory,file):
	os.chdir(directory)
	s = ftplib.FTP(host,username,password) # Connect
	f = open(file,'rb')                # file to send
	s.storbinary('STOR ' + file, f)         # Send the file

	f.close()                                # Close file and FTP
	s.quit()

# PATH VARIABLE MUST INCLUDE WHAT THE FILENAME WILL BE ON THE SERVER
def sftpup(host,username,password,file,path):
	ssh = paramiko.SSHClient() 
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
	ssh.connect(host, username=username, password=password)
	sftp = ssh.open_sftp()
	sftp.put(file,path,callback=None)
	sftp.close()
	ssh.close()	

