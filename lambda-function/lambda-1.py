import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    crawler_name = 'raw-data-crawler'

    try:
        state_response = glue.get_crawler(Name=crawler_name)
        crawler_state = state_response['Crawler']['State']

        if crawler_state == 'READY':
            glue.start_crawler(Name=crawler_name)
            return {
                'statusCode': 200,
                'body': f'Successfully started crawler: {crawler_name}'
            }
        else:
            return {
                'statusCode': 200,
                'body': f'Crawler is currently in state: {crawler_state}. Not starting again.'
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error starting crawler: {str(e)}'
        }
