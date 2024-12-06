import requests

# Pre-signed URL to download the file
#url = "https://spector-promostandard.s3.amazonaws.com/promostandard-document/tt_download.png?AWSAccessKeyId=AKIA2TY6XNI7ZNLK7K7J&Signature=cdxRAGvD9hCzElP%2FEo8DRf7LJ9E%3D&Expires=1728332711"
url = "https://spector-promostandard.s3.amazonaws.com/promostandard-document/test.jpg?AWSAccessKeyId=AKIAR377KUVZIQ7IIGPP&Signature=C8M78RZaSMLY7n0hYwboC47w9iQ%3D&Expires=1730133334"

# The file name you'd like to save the file as locally
local_file_path = "C:/aws_s3_dev/test.jpg"

# Download the file from the S3 URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the content to a local file
    with open(local_file_path, 'wb') as f:
        f.write(response.content)
    print(f"File downloaded successfully and saved as {local_file_path}")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
