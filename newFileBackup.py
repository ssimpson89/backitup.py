import transferProgram as do
import simplejson as json

# Get the API credentials
with open('creds.json', 'r') as f:
	creds = json.load(f)

archive = ""
savePath = ""

creds = creds['s3']
do = do.transfer.s3(creds["key"],creds["secret"])

do.list_all_my_buckets(creds["bucket"],) 