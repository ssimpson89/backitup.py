import ftplib
import os
import sys

def ftpup(host,username,password,directory,file):
	os.chdir(directory)
	s = ftplib.FTP(host,username,password) # Connect
	f = open(file,'rb')                # file to send
	s.storbinary('STOR ' + file, f)         # Send the file

	f.close()                                # Close file and FTP
	s.quit()

# PATH VARIABLE MUST INCLUDE WHAT THE FILENAME WILL BE ON THE SERVER
def sftpup(host,username,password,file,path):
    try:    
	    import paramiko
    except:
    	print("Paramiko is not installed. Visit lag.net/paramiko")
	ssh = paramiko.SSHClient() 
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
	ssh.connect(host, username=username, password=password)
	sftp = ssh.open_sftp()
	sftp.put(file,path,callback=None)
	sftp.close()
	ssh.close()	

def dropbox(local_file,remote_dir,remote_file,email,password):
	try:
		import mechanize
	except:
		print("Please install mechanize first")
	from dbconn import DropboxConnection
	conn = DropboxConnection(email, password)
	conn.upload_file(local_file,remote_dir,remote_file)
	print("File uploaded as " + remote_dir + remote_file)