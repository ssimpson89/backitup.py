import ftplib
import os
import sys
import urllib2
import re
import json

class transfer:
	class ftp:
		def up(self,host,username,password,directory,file):
			os.chdir(directory)
			s = ftplib.FTP(host,username,password) # Connect
			f = open(file,'rb')                # file to send
			s.storbinary('STOR ' + file, f)         # Send the file

			f.close()                                # Close file and FTP
			s.quit()
			
	class s3:
		class CallingFormat(object):
		    PATH = 1
		    SUBDOMAIN = 2
		    VANITY = 3
		    def build_url_base(protocol, server, port, bucket, calling_format):
		        url_base = '%s://' % protocol
		        if bucket == '':
		            url_base += server
		        elif calling_format == CallingFormat.SUBDOMAIN:
		            url_base += "%s.%s" % (bucket, server)
		        elif calling_format == CallingFormat.VANITY:
		            url_base += bucket
		        else:
		            url_base += server
		        url_base += ":%s" % port
		        if (bucket != '') and (calling_format == CallingFormat.PATH):
		            url_base += "/%s" % bucket
		        return url_base
		    build_url_base = staticmethod(build_url_base)
		
		DEFAULT_HOST = 's3.amazonaws.com'
		PORTS_BY_SECURITY = {True: 443, False: 80}
		METADATA_PREFIX = 'x-amz-meta-'
		AMAZON_HEADER_PREFIX = 'x-amz-'
		MAX_MEM_FILE_SIZE = 32 * 1024  # body size over this limit is spooled to disc

		def __init__(self, aws_access_key_id, aws_secret_access_key,
			is_secure=True, server=DEFAULT_HOST, port=None,
			calling_format=CallingFormat.SUBDOMAIN,
			spool_size=MAX_MEM_FILE_SIZE):
			if not port:
				port = self.PORTS_BY_SECURITY[is_secure]
			self.aws_access_key_id = aws_access_key_id
			self.aws_secret_access_key = aws_secret_access_key
			self.is_secure = is_secure
			self.server = server
			self.port = port
			self.calling_format = calling_format
			self.spool_size = spool_size		

		def create_bucket(self, bucket, headers=None):
			return Response(self._make_request('PUT', bucket, '', {}, headers))

		def check_bucket_exists(self, bucket):
			return self._make_request('HEAD', bucket, '', {}, {})

		def list_bucket(self, bucket, options=None, headers=None):
			return ListBucketResponse(self._make_request('GET', bucket, '', options, headers))

		def delete_bucket(self, bucket, headers=None):
			return Response(self._make_request('DELETE', bucket, '', {}, headers))

		def put(self, bucket, key, object, headers=None):
			if not isinstance(object, S3Object):
				object = S3Object(object)
				return Response(self._make_request('PUT', bucket, key, {}, headers, object.data, object.metadata))

		def get(self, bucket, key, headers=None):
			return GetResponse(self._make_request('GET', bucket, key, {}, headers),
			self.spool_size)

		def head(self, bucket, key, headers=None):
			return Response(self._make_request('HEAD', bucket, key, {}, headers))

		def delete(self, bucket, key, headers=None):
			return Response(self._make_request('DELETE', bucket, key, {}, headers))

		def get_bucket_logging(self, bucket, headers=None):
			return GetResponse(self._make_request('GET', bucket, '',
			{'logging': None}, headers))
	
		def put_bucket_logging(self, bucket, logging_xml_doc, headers=None):
			return Response(self._make_request('PUT', bucket, '',
			{'logging': None}, headers, logging_xml_doc))

		def get_bucket_acl(self, bucket, headers=None):
			return self.get_acl(bucket, '', headers)

		def get_acl(self, bucket, key, headers=None):
			return GetResponse(self._make_request('GET', bucket, key,
			{'acl': None}, headers))
	
		def put_bucket_acl(self, bucket, acl_xml_document, headers=None):
			return self.put_acl(bucket, '', acl_xml_document, headers)

		def put_acl(self, bucket, key, acl_xml_document, headers=None):
			return Response(self._make_request('PUT', bucket, key, {'acl': None},
			headers, acl_xml_document))

		def list_all_my_buckets(self, headers=None):
			return ListAllMyBucketsResponse(self._make_request('GET', '', '', {},
			headers))

		def get_bucket_location(self, bucket):
			return LocationResponse(self._make_request('GET', bucket, '',
			{'location': None}))






			
#	class sftp:
#		
#	class dropbox:
#		
#	class gdrive:
#		
#	class box:
#		