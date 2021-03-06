'''
This code finds the top 10 requested URLs along with count of number of times they have been requested using RDD approach
'''

import re
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("TopTenURL").getOrCreate()
sc = spark.sparkContext

apache_log_pattern = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)(.*)" (\d{3}) (\S+)'

def parse_log_line(log):
    m = re.match(apache_log_pattern, log)
    if m:
        return m.group(6)

logFile = sc.textFile("/data/spark/project/NASA_access_log_Aug95.gz")
urls = logFile.map(parse_log_line)
url_counts = urls.map(lambda url: (url, 1)).reduceByKey(lambda a, b: a + b)
url_counts.sortBy(lambda x:-x[1]).take(10)
