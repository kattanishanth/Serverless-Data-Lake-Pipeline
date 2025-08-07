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
            Message=f'The Glue job \"{job_name}\" was successfully started.'
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
