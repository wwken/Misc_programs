# Author: Ken Wu
# Date: 2017-10-16

from pyspark.sql import SparkSession

def addColumnIndex(df):
  old_column_names = df.columns[:]
  # Add Column index
  df = df.rdd.zipWithIndex().map(lambda (row, columnindex): (columnindex,) + row).toDF()
  df = df.withColumnRenamed('_1', 'rowIndex')
  for i in xrange(0, len(old_column_names)):
	# print ('old_column_names[i]', old_column_names[i])
  	df = df.withColumnRenamed('_' + str(i + 2), old_column_names[i])
  return df

inupt_file = "./data.csv"

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df1 = spark.read.format('csv').option("header", "true").option("mode", "DROPMALFORMED").load(inupt_file)
df1 = addColumnIndex(df1)

df2 = spark.read.format('csv').option("header", "true").option("mode", "DROPMALFORMED").load(inupt_file)
df2 = df2.withColumnRenamed('step', 'nextStep')
# shift all rows one up (i.e. discard the first row)
df2 = df2.rdd.zipWithIndex().filter(lambda (row, index): index > 0).keys().toDF()
df2 = addColumnIndex(df2)

dff = df1.join(df2, df1.rowIndex == df2.rowIndex, 'inner')	# join by the new added columnindex column

each_step_df = dff.groupby('step').count().withColumnRenamed('count', 'parent_count').withColumnRenamed('step', 'parent_step')
each_next_step_df = dff.groupby('step', 'nextStep').count().withColumnRenamed('count', 'child_count')

dfff = each_step_df.join(each_next_step_df, each_step_df.parent_step == each_next_step_df.step)
dfff = dfff.withColumn('chance', dfff.child_count / dfff.parent_count)

# pick the final columns to show
dfff = dfff.select('parent_step', 'nextStep', 'chance')

final_calculations = {}
for row in dfff.rdd.collect():
	if row.parent_step not in final_calculations:
		final_calculations[row.parent_step] = {}
	final_calculations[row.parent_step][row.nextStep] = str(row.chance * 100) + '%'

print 'Here is the final calculations:'

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
