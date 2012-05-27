import ftplib
import os.chdir

def ftpup(host,username,password,directory,file):
	os.chdir(directory)
	s = ftplib.FTP(host,username,password) # Connect
	f = open(file,'rb')                # file to send
	s.storbinary('STOR ' + file, f)         # Send the file

	f.close()                                # Close file and FTP
	s.quit()
	
