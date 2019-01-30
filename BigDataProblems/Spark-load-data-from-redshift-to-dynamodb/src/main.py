# How to run load data from redshift:
#
# 1) Download https://repository.mulesoft.org/nexus/content/repositories/public/com/amazon/redshift/redshift-jdbc42/1.2.1.1001/redshift-jdbc42-1.2.1.1001.jar
#
# 2) ```bash
# export PYTHONPATH=$PYTHONPATH:~/src/
# ```
#
# 3) Run spark-submit
# ```bash
# /usr/lib/spark/bin/spark-submit  --packages com.databricks:spark-redshift_2.11:3.0.0-preview1 --jars /home/kwu/RedshiftJDBC42-1.2.16.1027.jar --queue DE_high_priority ~/src/main.py
# ```


from pyspark.sql import SQLContext
from pyspark import SparkContext
import os
import boto3
from botocore.exceptions import ClientError
from time import sleep
from datetime import datetime, timedelta

# If run on local, export SPARK_MASTER_MODE=local[3]
# Otherwise, leave the env SPARK_MASTER_MODE blank
RETRY_EXCEPTIONS = ('ProvisionedThroughputExceededException',
                    'ThrottlingException')
table_name = 'table-1'


def update_record(profile_id, profile_type, v):
    if not v:
        return
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    retries = 1
    while True:
        try:
            table.update_item(
                Key={
                    'profile_id': profile_id,
                    'profile_type': profile_type
                },
                UpdateExpression="ADD content :element",
                ExpressionAttributeValues={
                    ':element': set([v])
                },
                ReturnValues="UPDATED_NEW"
            )
            return
        except ClientError as err:
            if err.response['Error']['Code'] not in RETRY_EXCEPTIONS:
                raise
            print('WHOA, too fast, slow it down retries={}'.format(retries))
            sleep(2 ** retries)
            retries += 1  # TODO max limit
    return


def get_start_date(num_of_days_before=0):
    return os.getenv('xxxxxx', datetime.strftime(datetime.now() - timedelta(num_of_days_before),
                                                                 '%Y-%m-%d'))


app_name = 'Load-data-from-redshift-to-DynamoDB'
start_date = get_start_date(1)
query = """
            REDSHIFT-SQL-QUERY-GOES-HERE
    """.format(start_date=start_date)

sc = SparkContext(os.getenv('SPARK_MASTER_MODE', 'yarn'), app_name)

sc = SQLContext(sc)
df = sc.read \
    .format("com.databricks.spark.redshift") \
    .option("url", "jdbc:redshift://xxxxxxxx:5439/dbname?user=kwu&password=xxxxx") \
    .option("forward_spark_s3_credentials", "true") \
    .option("query", query) \
    .option("tempdir", "s3n://tmp-ken/data") \
    .load()


def f(iterator):
    for row in iterator:
        profile_id = row['profile_id']
        client_type = row['client_type']
        device_name = row['device_name']
        device_id = row['device_id']
        ip = row['c_ip']
        print('inserting {} {} {} {} {}'.format(profile_id, client_type, device_name, device_id, ip))
        profile_type = 'GAID'   # by default, andriod phone
        if client_type == 'iphone':
            profile_type = 'IDFA'
        update_record(profile_id, profile_type, device_id)

        # Now insert the email
        update_record(profile_id, 'ip', ip)

df.foreachPartition(f)

