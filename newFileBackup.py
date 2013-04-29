import transferProgram as do
import simplejson as json

# Get the API credentials
with open('creds.json', 'r') as f:
	creds = json.load(f)

archive = ""
savePath = ""

do = do.transfer.s3()
creds = creds['s3']

do.ls(creds["bucket"],creds["key"],creds["secret"]) 