import boto3

# Initialize S3 client
s3_client = boto3.client('s3')

def generate_presigned_urls_for_folder(bucket_name, folder_name, expiration=3600):
    # List all objects in the folder
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
folder_name = 'promostandard-document'  # Make sure to include the trailing slash
expiration = 3600  # URL expiration time in seconds

urls = generate_presigned_urls_for_folder(bucket_name, folder_name, expiration)
for item in urls:
    print(f"File: {item['file_name']}, URL: {item['url']}")
