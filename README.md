# Serverless Data Lake Pipeline with AWS Glue, Lambda, and S3

## 📌 Project Overview

This project demonstrates how to build a **serverless data lake architecture** using AWS services such as **S3, Lambda, Glue (Crawler + ETL Job), CloudWatch Events, and SNS**. It automates the ingestion, cataloging, transformation, and notification pipeline for CSV files uploaded to S3, converting them into structured formats and storing them for downstream use.

---

## 🧠 Architecture Overview

### 🔄 Workflow Steps

1. **Raw Data Upload**: User uploads a CSV file (e.g., `marvel.csv`) to the **Raw S3 Bucket**.
2. **S3 Trigger**: Upload event triggers a **Lambda function**, which starts the **Glue Crawler**.
3. **Glue Crawler**: Scans the raw data and catalogs it in the **Glue Data Catalog**.
4. **CloudWatch Rule**: After crawler completion, a **CloudWatch Event Rule** triggers another Lambda function.
5. **Trigger ETL Job**: This second Lambda function starts a **Glue ETL Job**.
6. **ETL Job**: Transforms CSV into **Parquet format** and writes it to the **Processed S3 Bucket**.
7. **Notification**: A second CloudWatch rule detects job completion and triggers **SNS** to send an **email notification**.

---

### 🖼️ Architecture Diagram

![Architecture Diagram](screenshots/architecture-diagram.png)

---

## 🧰 Tools & AWS Services Used

| Service         | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| **S3**          | Store raw and processed CSV/Parquet data                                |
| **AWS Lambda**  | Trigger Glue crawler and ETL job                                        |
| **AWS Glue**    | Crawler to catalog raw data, ETL job to convert to Parquet              |
| **CloudWatch Events** | Detect completion of crawler/job and trigger actions               |
| **SNS**         | Send notification email after ETL success                               |
| **IAM**         | Grant roles and permissions for Lambda, Glue, and SNS access            |
| **Boto3**       | Python SDK used in Lambda for service interaction                       |

---

## 🧬 Directory Structure

```
Serverless-Data-Lake-Pipeline/
│
├── data/                          # Input CSV files (marvel.csv, dc.csv, etc.)
│
├── lambda-function/
│   ├── lambda-1.py                # Trigger Glue Crawler from S3 event
│   └── lambda-2.py                # Trigger Glue ETL job from CloudWatch rule
│
├── glue-job-script/
│   └── etl-job.py                 # Glue ETL job to transform CSV → Parquet
│
├── screenshots/                  # AWS Console screenshots of all components
│   ├── raw-bucket.png
│   ├── crawler.png
│   ├── catalog-table.png
│   ├── etl-job.png
│   ├── processed-bucket.png
│   ├── lambda1.png, lambda2.png
│   ├── lambda1-log.png, lambda2-log.png
│   ├── sns-subscription.png
│   ├── email-notification.png
│
└── README.md                     # This file
```

---

## 🧪 Lambda Function 1: Trigger Glue Crawler

```python
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    glue.start_crawler(Name='my-crawler-name')
    return {'statusCode': 200, 'body': 'Crawler triggered'}
```

- Trigger: S3 upload (e.g., `marvel.csv`)
- Starts the Glue crawler

---

## 🕷️ Glue Crawler

- **Name**: `my-crawler-name`
- **Data Catalog**: Automatically registers tables in your Glue database
- **Source**: Raw S3 bucket with CSV files

---

## 🔁 Lambda Function 2: Trigger Glue ETL Job

```python
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    glue.start_job_run(JobName='my-etl-job')
    return {'statusCode': 200, 'body': 'ETL job triggered'}
```

- Triggered by CloudWatch rule on crawler completion
- Starts Glue ETL job

---

## 🧪 Glue ETL Job

- **Name**: `my-etl-job`
- Reads from the Glue Data Catalog
- Converts CSV to Parquet
- Writes to `processed` S3 bucket

---

## 📩 Notification via SNS

- SNS Topic triggers after job completion
- Sends email to subscribed addresses with success message

---

## 📷 Screenshots

| Screenshot | Description                    |
|-----------|--------------------------------|
| raw-bucket.png | Uploaded raw files in S3   |
| crawler.png | AWS Glue Crawler console      |
| catalog-table.png | Table created by crawler |
| etl-job.png | Glue ETL job interface        |
| processed-bucket.png | Parquet data in S3   |
| lambda1.png / lambda2.png | Lambda function UI |
| lambda1-log.png / lambda2-log.png | CloudWatch logs |
| sns-subscription.png | SNS topic and subscriber |
| email-notification.png | Email confirmation |

---

## 🚀 How to Run

1. Upload CSV to Raw Bucket
2. Lambda1 triggers → Crawler starts
3. Crawler finishes → Lambda2 triggers
4. ETL Job runs → Data transformed → Notification sent

---

## 📧 Author

**Nishanth Katta**  
Project: Serverless Data Lake with AWS  
Email: [your_email@example.com]