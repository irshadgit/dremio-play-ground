from pyspark.sql import SparkSession
from pyspark import SparkConf
import os

def main():
    spark = SparkSession.builder.appName("spark-minio").enableHiveSupport().getOrCreate()

    spark.sparkContext.setLogLevel("DEBUG")

    print("Hurrayyyyyyyyyyy -", spark.sparkContext._jsc.hadoopConfiguration().get("fs.s3a.endpoint"))
    print("Hurrayyyyyyyyyyy -", spark.sparkContext._jsc.hadoopConfiguration().get("hive.metastore.uris"))
    
    data_lake_bucket_name = os.getenv('DATALAKE_BUCKET_NAME','data-lake')
    data_set_csv = os.getenv('DATA_SET_CSV_FILE_NAME','employee_details.csv')
    input_path = f"s3a://{data_lake_bucket_name}/{data_set_csv}"

    print("hurrrrrrrrrray")

    df = spark.read.csv(input_path)
    df.write.mode("overwrite").saveAsTable("default.")
    df.show()

    print("helooooooooooooooo")

if __name__ == "__main__":
    main()
