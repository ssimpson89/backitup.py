import ftplib
import os
import sys
import urllib2
import re
import json

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

######## DROPBOX CONNECTION ########
class dbup:
	email = ""
	password = ""
	root_ns = ""
	token = ""
	browser = None
	    
	def __init__(self,email,password):
		try:
			import mechanize
		except:
			print("Please install mechanize first")
		self.email = email
		self.password = password
		self.login()
		self.get_constants()

	def login(self):
		try:
			import mechanize
		except:
			print("Please install mechanize first")
		""" Login to Dropbox and return mechanize browser instance """
	        
		# Fire up a browser using mechanize
		self.browser = mechanize.Browser()
		self.browser.set_handle_robots(False)
	        
		# Browse to the login page
		self.browser.open('https://www.dropbox.com/login')
	        
		# Enter the username and password into the login form
		isLoginForm = lambda l: l.action == "https://www.dropbox.com/login" and l.method == "POST"
	        
		try:
			self.browser.select_form(predicate=isLoginForm)
		except:
			self.browser = None
			raise(Exception('Unable to find login form'))
	        
		self.browser['login_email'] = self.email
		self.browser['login_password'] = self.password
	        
		# Send the form
		response = self.browser.submit()
	        
	def get_constants(self):
		try:
			import mechanize
		except:
			print("Please install mechanize first")
		""" Load constants from page """
	        
		home_src = self.browser.open('https://www.dropbox.com/home').read()
	        
		try:
			self.root_ns = re.findall(r"root_ns: (\d+)", home_src)[0]
			self.token = re.findall(r"TOKEN: '(.+)'", home_src)[0]
		except:
			raise(Exception("Unable to find constants for AJAX requests"))

	def upload_file(self,local_file,remote_dir,remote_file):
		try:
			import mechanize
		except:
			print("Please install mechanize first")
		""" Upload a local file to Dropbox """
	        
		if(not self.is_logged_in()):
			raise(Exception("Can't upload when not logged in"))
	        self.browser.open('https://www.dropbox.com/')
	    
	        # Add our file upload to the upload form
	        isUploadForm = lambda u: u.action == "https://dl-web.dropbox.com/upload" and u.method == "POST"
	    
	        try:
	            self.browser.select_form(predicate=isUploadForm)
	        except:
	            raise(Exception('Unable to find upload form'))
	            
	        self.browser.form.find_control("dest").readonly = False
	        self.browser.form.set_value(remote_dir,"dest")
	        self.browser.form.add_file(open(local_file,"rb"),"",remote_file)
	        
	        # Submit the form with the file
	        self.browser.submit()
	def is_logged_in(self):
		try:
			import mechanize
		except:
			print("Please install mechanize first")
		""" Checks if a login has been established """
		if(self.browser):
			return True
		else:
			return False
########END DROPBOX########

#S3 Connection
def s3up(s3Bucket,s3Key,s3Secret,file,path):
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


