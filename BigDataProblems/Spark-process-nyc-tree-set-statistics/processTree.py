# Author: Ken Wu
# Date: 2018-09-15

# This pyspark program mainly demostrate the usage of the dataframe and the pyspark udf function examples that i encountered at work.
#  The dataset that this program was using had been changed to public data instead

from pyspark import SparkContext
from pyspark.sql import SQLContext
from functools import reduce
import pandas as pd
import numpy as np
from pyspark.sql.functions import col, collect_list, udf
from pyspark.sql.types import StringType

sc = SparkContext('local','example')  # if using locally
sql_sc = SQLContext(sc)

input_file = './2015StreetTreesCensus_TREES.csv'
# input_file = './2015StreetTreesCensus_TREES_small.csv'
pandas_df = pd.read_csv(input_file, sep=",", delimiter=",")  # assuming the file contains a header
pandas_df = pandas_df.replace(np.nan, '', regex=True)   # there are some empty columns (internally interpreted as nan inside dataframe) in the file that caused exceptions so need to map it to an empty string
pandas_df = pandas_df[['created_at', 'block_id', 'spc_common']]

pandas_df = sql_sc.createDataFrame(pandas_df)

created_at_block_id_summaries = pandas_df.groupby(['created_at', 'block_id'])


# Use udf to define a row-at-a-time udf
def myFunc(data_list):
    count = len(data_list)
    output = reduce(lambda x, y: x + ',' + y, data_list)
    return "{} {}".format(count, output)

myUdf = udf(myFunc, StringType())

created_at_block_id_summaries = created_at_block_id_summaries.agg(collect_list('spc_common').alias('spc_common')).withColumn('spc_common', myUdf('spc_common'))

# created_at_block_id_summaries.head(50)  # take the first 100 rows

created_at_block_id_summaries.show()