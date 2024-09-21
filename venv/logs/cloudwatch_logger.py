import time
import boto3

def log_to_cloudwatch(log_group, log_stream, message):
    client = boto3.client('logs')
    
    try:
        response = client.describe_log_streams(logGroupName=log_group)
        log_stream_name = response['logStreams'][0]['logStreamName']
        client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': int(round(time.time() * 1000)),
                'message': message
            }]
        )
        return "Logged successfully"
    except Exception as e:
        return str(e)
