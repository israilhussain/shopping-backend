import boto3
import uuid
import os

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_client = boto3.client("s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_image_to_s3(file):
    """Uploads an image file to S3 and returns the S3 URL."""
    file_extension = file.filename.split(".")[-1]
    file_key = f"products/{uuid.uuid4()}.{file_extension}"
    
    s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file_key)

    s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
    return s3_url
