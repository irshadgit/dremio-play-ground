from pyspark.sql import SparkSession
from pyspark import SparkConf
import os

def main():
    spark = SparkSession.builder.appName("spark-minio").getOrCreate()

    spark.sparkContext.setLogLevel("DEBUG")
    spark._jsc.hadoopConfiguration().set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY", "minio"))
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.getenv("AWS_SECRET_KEY", "minio123"))
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.getenv("AWS_S3A_END_POINT", "http://minio.play-ground.svc.cluster.local:80"))

    print("Hurrayyyyyyyyyyy -", spark.sparkContext._jsc.hadoopConfiguration().get("fs.s3a.endpoint"))

    source_bucket = "my-test"
    input_path = f"s3a://{source_bucket}/test.json"

    print("hurrrrrrrrrray")

    df = spark.read.json(input_path)
    df.show()

    print("helooooooooooooooo")

if __name__ == "__main__":
    main()
