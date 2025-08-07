# 📦 Serverless Data Lake Pipeline with AWS Glue, Lambda, and S3

## 🚀 Project Overview

This project demonstrates how to build a **serverless data lake** using AWS services like **S3, Glue, Lambda, EventBridge**, and **SNS**. The pipeline ingests raw CSV files, processes them into Parquet format using AWS Glue ETL, and stores the results in an S3 bucket. The whole flow is event-driven and automated via Lambda and EventBridge rules, with final notifications sent via SNS.

## 🧭 Architecture

### High-Level Flow

1. **Raw Data Upload**: CSV files (e.g., `avengers.csv`, `marvel.csv`, `dc.csv`) are uploaded into the raw S3 bucket.
2. **Lambda Trigger**: An S3 PUT event triggers `lambda-1.py`, which starts the Glue Crawler.
3. **Glue Crawler**: Catalogs the uploaded data to the AWS Glue Data Catalog.
4. **EventBridge Rule**: On crawler success, EventBridge triggers `lambda-2.py` to initiate the Glue ETL job.
5. **Glue ETL Job**: Converts CSV to Parquet and stores results in the processed S3 bucket.
6. **Final Notification**: After ETL success, an SNS notification is sent to subscribed users.

### 📊 Architecture Diagram

![Architecture Diagram](A_flowchart_diagram_on_a_grid_background_illustrat.png)

---

## 🔧 Tools and Technologies Used

- **Amazon S3**: Raw and processed data storage.
- **AWS Lambda**: Triggers Glue jobs and crawlers.
- **AWS Glue**: Data cataloging (Crawler) and transformation (ETL).
- **AWS EventBridge**: Monitors Glue events and triggers ETL jobs.
- **Amazon SNS**: Sends notifications.
- **Python & Boto3**: Used inside Lambda scripts.
- **AWS IAM**: Manages roles and permissions.

---

## 🛠️ Project Components

### 📂 Buckets Used

- `nishanth-raw-bucket`: For CSV file uploads.
- `nishanth-processed-bucket`: For storing Parquet output.
- `nishanth-athena-results`: For Athena query results.

### 🧠 AWS Glue Crawler

```json
{
  "crawlerName": "raw-data-crawler",
  "database": "nishanth-database"
}
```

### 🐍 Lambda Function 1 – Start Crawler (`lambda-1.py`)

```python
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    crawler_name = 'raw-data-crawler'

    try:
        state = glue.get_crawler(Name=crawler_name)['Crawler']['State']
        if state != 'READY':
            return {
                'statusCode': 200,
                'body': f'Crawler is currently in state: {state}. Not starting again.'
            }

        glue.start_crawler(Name=crawler_name)
        return {
            'statusCode': 200,
            'body': f'Successfully started crawler: {crawler_name}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error starting crawler: {str(e)}'
        }
```

### 🎯 EventBridge Rule – Crawler Success

```json
{
  "source": ["aws.glue"],
  "detail-type": ["Glue Crawler State Change"],
  "detail": {
    "crawlerName": ["raw-data-crawler"],
    "state": ["Succeeded"]
  }
}
```

### 🐍 Lambda Function 2 – Start Glue ETL Job (`lambda-2.py`)

```python
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    sns = boto3.client('sns')

    job_name = 'csv-parquet-job'
    sns_topic_arn = 'arn:aws:sns:us-east-1:011547836001:glue-notification'

    try:
        glue.start_job_run(JobName=job_name)
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject='Glue Job Started',
            Message=f'The Glue job "{job_name}" was successfully started.'
        )
        return {
            'statusCode': 200,
            'body': f'Successfully started Glue job: {job_name}'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error starting Glue job: {str(e)}'
        }
```

### 🔁 Glue ETL Script – `etl-job.py`

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource = glueContext.create_dynamic_frame.from_catalog(
    database="nishanth-database", 
    table_name="raw_data", 
    transformation_ctx="datasource"
)

datasink = glueContext.write_dynamic_frame.from_options(
    frame=datasource,
    connection_type="s3",
    connection_options={"path": "s3://nishanth-processed-bucket/"},
    format="parquet",
    transformation_ctx="datasink"
)

job.commit()
```

---

## 📬 SNS Notification

- **Topic Name**: `glue-notification`
- **Action**: Sends email on Glue ETL success.

---

## ✅ Output Validation

- **Athena**: Query the final Parquet files from `nishanth-processed-bucket`
- **SNS Email**: Confirms job completion
- **Logs**: Available via CloudWatch Logs for both Lambda functions

---

## 📁 Screenshots

Screenshots of each AWS service setup and pipeline step are included in the `/screenshots` folder.

---

## 📌 Conclusion

This project builds a **completely serverless data lake** pipeline using core AWS services, with no manual triggers. Ideal for automation, learning serverless patterns, and production-grade ingestion workflows.