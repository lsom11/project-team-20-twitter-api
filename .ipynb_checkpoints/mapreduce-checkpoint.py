from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col

tweet_file = "data/tweets.csv"
spark = SparkSession.builder.appName("MapReducer").getOrCreate()

schema = StructType([
    StructField("target", IntegerType(), True),
    StructField("id", IntegerType(), True),
    StructField("date", StringType(), True),
    StructField("flag", StringType(), True),
    StructField("user", StringType(), True),
    StructField("text", StringType(), True)
])


tweet_data = spark.read.csv(tweet_file, header=False, schema=schema)
tweet_data = tweet_data.dropDuplicates()

filter_terms = ['test']
f = tweet_data["text"] in filter_terms
print(f)
# filtered_tweets = tweet_data[f]
# filtered_tweets = tweet_data.filter(col("text") in filter_terms)
# filtered_tweets.show(10)
# filtered_tweets.count()

spark.stop()