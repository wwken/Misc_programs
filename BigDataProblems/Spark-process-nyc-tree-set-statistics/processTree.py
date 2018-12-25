# Author: Ken Wu
# Date: 2018-09-15

# This pyspark program mainly demostrate the usage of the dataframe and the pyspark udf function examples that i encountered at work.
#  The dataset that this program was using had been changed to public data instead

from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SQLContext
from functools import reduce
import pandas as pd
import numpy as np
from pyspark.sql.functions import col, collect_list, udf
from pyspark.sql.types import StringType
import logging
import time

app_name = 'Spark-process-nyc-tree-set-statistics'
logger = logging.getLogger(app_name)

###############################################################################################################
## main-program:
###############################################################################################################

def run_spark_job():

    ###############################################################################################################
    ## utility functions:
    ###############################################################################################################

    # print spark configurations
    def printSparkConfigurations():
        c = SparkConf()
        print("Spark configurations: {}".format(c.getAll()))

    # Use udf to define a row-at-a-time udf
    def myFunc(data_list):
        count = len(data_list)
        output = reduce(lambda x, y: x + ',' + y, data_list)
        return "{} {}".format(count, output)

    sql_sc = SQLContext(SparkContext('local',app_name))

    printSparkConfigurations()

    # input_file = './2015StreetTreesCensus_TREES.csv'
    input_file = './2015StreetTreesCensus_TREES_small.csv'
    pandas_df = pd.read_csv(input_file, sep=",", delimiter=",")  # assuming the file contains a header

    pandas_df.repartition('created_at')     # optimization trick !

    pandas_df = pandas_df.replace(np.nan, '', regex=True)   # there are some empty columns (internally interpreted as nan inside dataframe) in the file that caused exceptions so need to map it to an empty string
    pandas_df = pandas_df[['created_at', 'block_id', 'spc_common']]

    pandas_df = sql_sc.createDataFrame(pandas_df)

    created_at_block_id_summaries = pandas_df.groupby(['created_at', 'block_id'])

    myUdf = udf(myFunc, StringType())

    created_at_block_id_summaries = created_at_block_id_summaries.agg(collect_list('spc_common').alias('spc_common')).withColumn('spc_common', myUdf('spc_common'))

    # created_at_block_id_summaries.head(50)  # take the first 100 rows

    created_at_block_id_summaries.show()

def simulate_component(compID, run_f):
    """
    Do simulation for the specified foreground component.
    """
    logger.info("==================================================")
    logger.info(">>> Simulate component: %s <<<" % compID)
    logger.info("==================================================")
    t1_start = time.perf_counter()
    t2_start = time.process_time()

    run_f()

    t1_stop = time.perf_counter()
    t2_stop = time.process_time()
    logger.info("--------------------------------------------------")
    logger.info("Elapsed time: %.1f [min]" % ((t1_stop - t1_start) / 60))
    logger.info("CPU process time: %.1f [min]" % ((t2_stop - t2_start) / 60))
    logger.info("--------------------------------------------------")

simulate_component(app_name, run_spark_job)