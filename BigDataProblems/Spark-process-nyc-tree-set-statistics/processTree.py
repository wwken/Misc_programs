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
from pyspark.sql.functions import collect_list, udf
from pyspark.sql.types import StringType
import time

app_name = 'Spark-process-nyc-tree-set-statistics'

###############################################################################################################
## main-program:
###############################################################################################################

def run_spark_job(sc, run_N_times = 1):

    ###############################################################################################################
    ## utility functions:
    ###############################################################################################################

    def print_df(df, only_display=100):
        outout = df.collect()
        for idx, o in enumerate(outout):
            if idx > only_display:
                print(' And more ...')
                break
            print(o)

    # print spark configurations
    def printSparkConfigurations():
        c = SparkConf()
        print("Spark configurations: {}".format(c.getAll()))

    # Use udf to define a row-at-a-time udf
    def myFunc(data_list):
        s = set()
        for d in data_list:
            s.add(d)
        count = len(s)
        output_str = reduce(lambda x,y: x+', '+y, s)
        return "{} {}".format(count, output_str)

    def read_csv_in_chunk(input_file):
        def optimize_chunk(chunk, column_names):
            for n in column_names:
                chunk[n] = chunk[n].astype('category')
            return chunk

        df = pd.DataFrame()
        chunk_size = 50000
        for idx, chunk in enumerate(pd.read_csv(input_file, sep=",", delimiter=",", chunksize=chunk_size)):   # assuming the file contains a header
            print("Reading the csv input in chunk index: {} on chunk_size: {} ".format(idx, chunk_size))
            # optimize the rows by changing it to category type
            chunk = optimize_chunk(chunk, ['trnk_wire', 'trnk_light', 'trnk_other', 'state', 'root_grate', 'root_other', 'root_stone', 'sidewalk', 'health', 'curb_loc', 'brnch_ligh', 'brnch_othe', 'brnch_shoe', 'guards',
                                           'user_type', 'status', 'steward', 'boroname', 'zip_city'])
            df = pd.concat([df, chunk], ignore_index=True)
        return df

    printSparkConfigurations()

    input_file = './2015StreetTreesCensus_TREES.csv'
    # input_file = './2015StreetTreesCensus_TREES_small.csv'
    pandas_df_raw = read_csv_in_chunk(input_file)

    for i in range(run_N_times):
        pandas_df = pandas_df_raw.replace(np.nan, '', regex=True)   # there are some empty columns (internally interpreted as nan inside dataframe) in the file that caused exceptions so need to map it to an empty string
        pandas_df = pandas_df[['created_at', 'block_id', 'spc_common']]

        pandas_df = sc.createDataFrame(pandas_df)

        pandas_df.repartition(5000, 'created_at')     # optimization trick !

        myUdf = udf(myFunc, StringType())

        created_at_block_id_summaries = pandas_df.groupby(['created_at', 'block_id']).agg(collect_list('spc_common').alias('spc_common')).withColumn('spc_common', myUdf('spc_common'))

        print_df(created_at_block_id_summaries)

        block_id_created_at_summaries = pandas_df.groupby(['block_id', 'created_at']).agg(collect_list('spc_common').alias('spc_common')).withColumn('spc_common', myUdf('spc_common'))

        print_df(block_id_created_at_summaries)


def simulate_component(sc, compID, run_f, env=None, run_N_times = 1):
    # log4jLogger = sc._jvm.org.apache.log4j
    # logger = log4jLogger.LogManager.getLogger(compID)
    """
    Do simulation for the specified foreground component.
    """
    print("==================================================")
    print(">>> Simulate component: %s at %s <<<" % (compID, env))
    print("==================================================")
    t1_start = time.perf_counter()
    t2_start = time.process_time()

    run_f(sc, run_N_times)

    t1_stop = time.perf_counter()
    t2_stop = time.process_time()
    print("--------------------------------------------------")
    print("Elapsed time: %.1f [min]" % ((t1_stop - t1_start) / 60))
    print("CPU process time: %.1f [min]" % ((t2_stop - t2_start) / 60))
    print("--------------------------------------------------")

env = "Ken's MBP"
sc = SQLContext(SparkContext('local',app_name))
run_N_times = 20
simulate_component(sc, app_name, run_spark_job, env, run_N_times)