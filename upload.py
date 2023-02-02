import boto3
from botocore.client import Config
import os

ENDPOINT = "https://storage.yandexcloud.net"
ACCESS_KEY = os.environ.get('YC_ACCESS_KEY')
SECRET_KEY = os.environ.get('YC_SECRET_KEY')
BUCKET_NAME = os.environ.get('YC_BUCKET_NAME')

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="ru-central1",
)
s3 = session.client(
    "s3", endpoint_url=ENDPOINT, config=Config(signature_version="s3v4")
)

presigned_url = s3.generate_presigned_post(BUCKET_NAME, 'test.png', ExpiresIn=3600)

for field in presigned_url['fields']:
    print(f"{field}:{presigned_url['fields'][field]}")
