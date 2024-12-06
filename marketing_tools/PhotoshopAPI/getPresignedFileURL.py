import boto3
from botocore.exceptions import NoCredentialsError

# Initialize a session using Amazon S3
s3 = boto3.client('s3',region_name='us-east-1')

# Bucket and object information
bucket_name = "spector-promostandard"
s3_file_key = "tt_download_return.png" 
#s3_file_key = "promostandard-document/tt_download_return.png"# The S3 object key (file path in the bucket)

# Generate a pre-signed URL for downloading the file (expires in 3600 seconds = 1 hour)
try:
    presigned_url = s3.generate_presigned_url('put_object',
                                              Params={'Bucket': bucket_name, 'Key': s3_file_key},
                                              ExpiresIn=3600)  # Time in seconds

    print(f"Pre-signed URL: {presigned_url}")

except NoCredentialsError:
    print("AWS credentials not found.")
