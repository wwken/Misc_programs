This PySpark job is to demostrate the use of PySpark DataFrame API with udf functions. 

and group by date and block id to find all distinct spc_common names using pyspark udf functions

The screenshot can be referred in the screenshot folder.

--To run:

1) Download the sample dataset from: take the input data from: https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/pi5s-9p35
    The file it should be downloaded is: 2015StreetTreesCensus_TREES.csv of about 250MB
    
2) Have the spark cluster ready.  For example, I used this Spark-ML-Vagrant vm for experiments to run: https://github.com/paulovn/ml-vm-notebook/

3) Run the processTree.py by doing spark-submit --queue default ./src/processTree.py 

