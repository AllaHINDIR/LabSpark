import re
import sys
from unittest.loader import VALID_MODULE_NAME
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType,IntegerType, FloatType, BooleanType
from pyspark.sql.functions import regexp_replace,col
import time

spark = SparkSession.builder\
			.master("local[1]")\
			.appName("SparkByExamples.com")\
			.getOrCreate()

# header to read automaticlly the first line (name of column)
# inferSchema : il déduit automatiquement les types de colonnes en fonction des données.
#df = spark.read.options(delimiter=',',header='True', inferSchema='True')\
	#.csv("./part-00000-of-00001.csv")

schema_machine_event = StructType() \
	.add("time",IntegerType(),True)\
      .add("machine ID",IntegerType(),True)\
			.add("event type",IntegerType(),True)\
				.add("platform ID",StringType(),True)\
					.add("CPUs",FloatType(),True)\
						.add("Memory",FloatType(),True)

df_with_schema_machine_event = spark.read.format("csv") \
      .option("header", False) \
      .schema(schema_machine_event) \
      .load("./part-00000-of-00001.csv")

#df_with_schema.printSchema()
#df_with_schema_machine_event.show()
print(df_with_schema_machine_event.count())

#Distribution of machine according to thier CPU capacity.
df2 = df_with_schema_machine_event.groupBy("CPUs").count().sort("count")
df2.show()

# distribution of the number of jobs/tasks per scheduling class

schema_task_event = StructType() \
	.add("time",IntegerType(),True)\
      .add("missing info",IntegerType(),True)\
			.add("job ID",IntegerType(),True)\
				.add("task index",IntegerType(),True)\
					.add("machine ID",IntegerType(),True)\
						.add("event type",IntegerType(),True)\
							.add("user",StringType(),True)\
								.add("schulding class",IntegerType(),True)\
									.add("priority",IntegerType(),True)\
										.add("CPU request",FloatType(),True)\
											.add("memory request",FloatType(),True)\
												.add("disk space request",FloatType(),True)\
													.add("different machine restriction",BooleanType(),True)

df_with_schema_task_event = spark.read.format("csv") \
      .option("header", False) \
      .schema(schema_task_event) \
      .load("./part-00000-of-00500.csv")
#df_with_schema_task_event.show()

df2_task_event = df_with_schema_task_event.groupBy("schulding class").count().sort("count")
df2_task_event.show()

schema_job_event = StructType() \
	.add("time",IntegerType(),True)\
      .add("missing info",IntegerType(),True)\
			.add("job ID",IntegerType(),True)\
						.add("event type",IntegerType(),True)\
							.add("user",StringType(),True)\
								.add("schulding class",IntegerType(),True)\
									.add("job name",StringType(),True)\
										.add("logical job name",StringType(),True)\

df_with_schema_job_event = spark.read.format("csv")\
	.option("header",False)\
		.schema(schema_job_event)\
			.load("part-00001-of-00500.csv")
df2_job_event = df_with_schema_job_event.groupBy("schulding class").count().sort("count")
df2_job_event.show()

#Do tasks with a low scheduling class have a higher probability of being evicted? : yes, because 
#A task or a job might also be EVICTed, for instance if high priority tasks have to be executed instead.
#and we have the number of tasks with 0 priority is less then the sum of tasks which have 1,...,11 priority 

df_task_priority = df_with_schema_task_event.groupBy("priority").count().sort("count")
df_task_priority.show()

#In general, do tasks from the same job run on the same machine? : 
# no, for exemple : job id = 1412625411| machine id = 1429192957 and job id = 1412625411| machine id = 537747619
df_task_job_machine = df_with_schema_task_event.groupBy("job ID","machine ID").count().sort("count")
df_task_job_machine.show()

