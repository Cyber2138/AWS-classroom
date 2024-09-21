import boto3

def upload_to_s3(file_name, bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        return f"File {file_name} uploaded successfully to {bucket_name}."
    except Exception as e:
        return str(e)
