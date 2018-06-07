# Author: Ken Wu
# Date: 2017-10-16

from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id

inupt_file = "./data.csv"

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df1 = spark.read.format('csv').option("header", "true").option("mode", "DROPMALFORMED").load(inupt_file)
df1 = df1.withColumn('id', monotonically_increasing_id())

df2 = spark.read.format('csv').option("header", "true").option("mode", "DROPMALFORMED").load(inupt_file)
df2 = df2.withColumnRenamed('step', 'nextStep')
df2 = df2.withColumn('id', monotonically_increasing_id())

# now union the two dataframes
dff = df1.join(df2, df1.id == df2.id - 1)

each_step_df = dff.groupby('step').count().withColumnRenamed('count', 'parent_count').withColumnRenamed('step', 'parent_step')
each_next_step_df = dff.groupby('step', 'nextStep').count().withColumnRenamed('count', 'child_count')

dfff = each_step_df.join(each_next_step_df, each_step_df.parent_step == each_next_step_df.step)
dfff = dfff.withColumn('chance', dfff.child_count / dfff.parent_count)

# pick the final columns to show
dfff = dfff.select('parent_step', 'nextStep', 'chance')

# print (dfff.schema)

final_calculations = {}
for row in dfff.rdd.collect():
	if row.parent_step not in final_calculations:
		final_calculations[row.parent_step] = {}
	final_calculations[row.parent_step][row.nextStep] = str(row.chance * 100) + '%'

# get the unique value
all_unique_step = []
df_unique = df1.groupby('step').count()
header_str = '------'
for row in df_unique.rdd.collect():
	all_unique_step.append(str(row.step))
	header_str += '--' + str(row.step) + '-- '
print header_str


for x in xrange(0, len(all_unique_step)):
	print_str = '--' + all_unique_step[x] + '-- '
	for y in xrange(0, len(all_unique_step)):
		chance = '00.0%'
		if all_unique_step[x] in final_calculations:
			if all_unique_step[y] in final_calculations[all_unique_step[x]]:
				chance = final_calculations[all_unique_step[x]][all_unique_step[y]]
		print_str += chance + ' '
	print print_str


spark.stop()
