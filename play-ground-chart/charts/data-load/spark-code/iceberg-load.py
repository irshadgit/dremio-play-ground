from pyspark.sql import SparkSession
from pyspark import SparkConf
import os
from pyspark.sql.functions import col

def main():
    spark = SparkSession.builder.appName("spark-minio").enableHiveSupport().getOrCreate()
    spark.sparkContext.setLogLevel("DEBUG")
    data_lake_bucket_name = os.getenv('DATALAKE_BUCKET_NAME','data-lake')
    data_set_csv = os.getenv('DATA_SET_CSV_FILE_NAME','daily_product_sales.csv')
    input_path = f"s3a://{data_lake_bucket_name}/{data_set_csv}"
    df = spark.read.option("header", "true").csv(input_path)
    formattedSalesDF = df.withColumn("date", col("date").cast("date"))
    spark.sql("CREATE DATABASE IF NOT EXISTS iceberg.iceberg")
    # Writing as iceberg table
    formattedSalesDF\
        .writeTo("iceberg.iceberg.daily_product_sales")\
        .partitionedBy(col("date"))\
        .createOrReplace()

    # Writing as table backed by parquet files
    spark.sql("CREATE DATABASE IF NOT EXISTS parquet")
    formattedSalesDF.write\
    .format("parquet")\
    .mode("overwrite")\
    .partitionBy("date")\
    .saveAsTable("parquet.daily_product_sales")

if __name__ == "__main__":
    main()
