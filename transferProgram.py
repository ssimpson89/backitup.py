import ftplib
import os
import sys
import urllib2
import re
import json

class transfer:
	class ftp:
		def up(host,username,password,directory,file):
			os.chdir(directory)
			s = ftplib.FTP(host,username,password) # Connect
			f = open(file,'rb')                # file to send
			s.storbinary('STOR ' + file, f)         # Send the file

			f.close()                                # Close file and FTP
			s.quit()
	class s3:
		def up(self,s3Bucket,s3Key,s3Secret,file,path):
			try:
				from boto.s3.connection import S3Connection
				from boto.s3.key import Key
			except:
				print("Please ensure boto is installed")
			os.chdir(path)
			conn = S3Connection(s3Key,s3Secret)
			b = conn.create_bucket(s3Bucket)
			k = Key(b)
			k.key = file
			k.set_contents_from_filename(file)
			k.set_contents_from_string(file)
			print(file + " has been uploaded to " + s3Bucket)