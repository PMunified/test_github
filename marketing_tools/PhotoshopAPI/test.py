import boto3
import requests

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration
    )
    return presigned_url

def upload_file_to_s3(presigned_url, file_path):
    with open(file_path, 'rb') as file:
        response = requests.put(presigned_url, data=file)
    
    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}")

def generate_presigned_urls_for_folder(bucket_name, folder_name, expiration=3600):
    # List all objects in the folder
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    
    if 'Contents' not in response:
        print(f"No files found in the folder '{folder_name}'")
        return []

    presigned_urls = []
    for obj in response['Contents']:
        object_name = obj['Key']
        
        # Generate a presigned URL for each file
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        presigned_urls.append({'file_name': object_name, 'url': url})
    
    return presigned_urls
# Usage
bucket_name = 'spector-promostandard'
folder_name = 'promostandard-document'
expiration = 3600  # URL expiration time in seconds
object_name = 'promostandard-document/test123.jpg'  # Path in the S3 bucket
file_path = 'C:/aws_s3_dev/1_EC153_v1727288531.jpg'  # Path to the file you want to upload

# Generate presigned URL
url = generate_presigned_url(bucket_name, object_name)
print(f"Presigned URL for upload: {url}")

# Upload the file
upload_file_to_s3(url, file_path)

urls = generate_presigned_urls_for_folder(bucket_name, folder_name, expiration)
for item in urls:
    print(f"File: {item['file_name']}, URL: {item['url']}")
