import psycopg2
import sys

leaflink_configuration = { 'dbname': 'database_name', 
                  'user':'user_name',
                  'pwd':'user_password',
                  'host':'redshift_endpoint',
                  'port':'redshift_password',
                  'aws_key': 'AKIAWXXXXXXXXXXXXXX',
                  'aws_secret': 'Y0JvWIuiXXXXXXXXXXXXXXXXXXXXX',
                  's3_bucket': 'leafliink-data-interview-exercise'
                }

def create_conn(*args,**kwargs):
    config = kwargs['config']
    try:
        conn=psycopg2.connect(dbname=config['dbname'], host=config['host'], port=config['port'], user=config['user'], password=config['pwd'])
    except Exception as err:
        print err.code, err
    return conn

def load_redshift_table(cursor, year, month, day, config):
	sql_create = """
	CREATE TABLE IF NOT EXISTS load_impressions_{year}{month}{day} (
		metaSchema		varchar(255),
		metaVersion	varchar(255),
		GdprComputed BOOLEAN,
		GdprSource	VARCHAR(255),
		RemoteIP	VARCHAR(255),
		UserAgent	VARCHAR(MAX),
		Ecpm	INT,
		Datacenter	BOOLEAN,
		BurnIn	BOOLEAN,
		IsValidUA	BOOLEAN,
		User_Key	VARCHAR(255),
		User_IsNew	BOOLEAN,
		UserKey 	VARCHAR(255),
		ImpressionCount	INT,		
		Id 	VARCHAR(255),
		DecisionId VARCHAR(255),
		DecisionIdx INT,
		CreatedOn VARCHAR(MAX),
		EventCreatedOn TIMESTAMP,
		ImpressionCreatedOn TIMESTAMP,
		AdTypeId INT,
		AuctionBids INT,
		BrandId INT,
		CampaignId INT,
		Categories VARCHAR(MAX),
		ChannelId INT,
		CreativeId INT,
		CreativePassId INT,
		DeliveryMode INT,
		Device_brandName VARCHAR(255),
		Device_modelName VARCHAR(255),
		Device_osRawVersion INT,
		Device_osMajorVersion INT,
		Device_osMinorVersion INT,
		Device_browser VARCHAR(255),
		Device_browserRawVersion FLOAT4,
		Device_browserMajorVersion 	INT,
		Device_browserMinorVersion 	INT,
		Device_formFactor VARCHAR(255),
		FirstChannelId INT,
		IsNoTrack 	BOOLEAN,
		IsTrackingCookieEvents  	BOOLEAN,
		IsPublisherPayoutExempt BOOLEAN,
		Keywords VARCHAR(MAX),
		MatchingKeywords VARCHAR(255),
		NetworkId 	INT,
		PassId 	INT,
		PhantomCreativePassId 	INT,
		PlacementName VARCHAR(255),
		PhantomPassId 	INT,
		PriorityId	INT,
		Price VARCHAR(32),
		RateType 	INT,
		RelevancyScore INT,
		Revenue 	INT,
		NetRevenue	INT,
		GrossRevenue	INT,
		ServedBy VARCHAR(255),
		ServedByPid	INT,
		ServedByAsg VARCHAR(255),
		SiteId	INT,
		Url VARCHAR(MAX),
		ZoneId INT
	) DISTKEY (UserKey);

	delete from load_impressions_{year}{month}{day};

	copy load_impressions_{year}{month}{day}
	from 's3://{s3_bucket}/{day}'
	json 's3://{s3_bucket}/leaflink_jsonpath.json';

	""".format(year=year, 
		month=month, 
		day=day, 
		s3_bucket=config.s3_bucket,
		aws_key=config.aws_key,
		aws_secret=config.aws_secret)
	try:
		cursor.execute(sql_create)
	except Exception as err
		print err.code,err

# Here the program execution
if len(sys.argv) != 2:
	print("Please provide one argument - the date of the directory, e.g. 02 or 03")
	sys.exit(1)

load_year = '2020'
load_month = '02'			# Assume it is febuary 02, that is what i saw in the s3 buckets the files are prefixed by 02_XX
load_day = sys.argv[1]
print('Now running the load data on the folder: {}'.format())

conn = create_conn(config=leaflink_configuration)
cursor = conn.cursor()
load_redshift_table(cursor, load_year, load_month, load_day, 
	leaflink_configuration)



