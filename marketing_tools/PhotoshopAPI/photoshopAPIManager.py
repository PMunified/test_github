import os,time
import requests,json
from dotenv import load_dotenv
import boto3

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def getAccessToken(id, secret):

	response = requests.post(f"https://ims-na1.adobelogin.com/ims/token/v2?client_id={id}&client_secret={secret}&grant_type=client_credentials&scope=openid,AdobeID,read_organizations")
	return response.json()

def sayHello(id, token):
	response = requests.get(f"https://image.adobe.io/pie/psdService/hello", headers = {"Authorization": f"Bearer {token}", "x-api-key": id })
	return response.text

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration
    )
    return presigned_url
# Function to check the status of the job
def check_status(access_token,api_key,status_url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": api_key
    }
    
    # Make the GET request to check job status
    response = requests.get(status_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        status_data = response.json()
        # If 'output' link is present, the job is completed
        if 'output' in status_data.get('_links', {}):
            print("Job completed. Download URL:", status_data['_links']['output']['href'])
            return True
        else:
            print("Job still processing...")
    else:
        print(f"Error: {response.status_code}, {response.text}")
    
    return False

# Poll the job status until it's complete

#print("Job polling finished.")

def remove_background_from_image(access_token,image_url, output_file_path):
    url = "https://image.adobe.io/sensei/cutout"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": CLIENT_ID,
        "Content-Type": "application/json",
    }

    payload = {
          "input": {
          "href": image_url, 
          "storage": "external"
        },
        "options": {
            "optimize": "performance",
            "process": {
                "postprocess": True
            },
            "service": {
                "version": "4.0"
            }
        },      
        "output": {
          "href": generate_presigned_url('spector-promostandard','promostandard-document/test.png'),
          "storage": "external",
          "type": "image/png",
          "color": {
            "space": "rgb"
            },          
          "mask":{
              "format":"soft"
            }
        }        
    }   

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 202:
        # Extract the status URL (assuming it's in the Location header)
        jsonObject = json.loads(response.text)
        status_url = jsonObject['_links']['self']['href']#response.headers.get("Location")
    
        if status_url:
            print(f"Operation is in progress. Checking status at: {status_url}")
        
            # Poll the status URL until the operation completes
            while True:
                status_response = requests.get(status_url, headers=headers)
            
                if status_response.status_code == 200:
                    # The operation is complete
                    print("Operation completed successfully!")
                    # Process the final response if needed
                    #print(status_response.json())
                    status_data = status_response.json()
                    print("Job Status:", status_data['status'])
                    if status_data['status'] == 'completed':
                        print("Job completed.")
                        break
                    elif status_data['status'] == 'failed':
                        print("Job failed.")
                        print(status_data)
                        break
                    time.sleep(1)                     
                    #break
                elif status_response.status_code == 202:
                    # Still processing; wait and try again
                    print("Operation still in progress. Checking again in 5 seconds...")
                    time.sleep(5)  # Wait for 5 seconds before checking again
                else:
                    # Handle unexpected status codes
                    print(f"Unexpected response: {status_response.status_code}")
                    break
        else:
            print("No status URL returned. Something went wrong.")    
    elif response.status_code == 404:
        print(f"Error 404: Not Found. Check the endpoint URL or image URL.")
    else:
        print(f"Error: {response.status_code}, {response.text}")


token = getAccessToken(CLIENT_ID, CLIENT_SECRET)['access_token']

#response = sayHello(CLIENT_ID, token)
#print(f"Response from hello endpoint: {response}")

#image_url = "https://www.spectorandco.com/product_images/products/1_EC153_v1727288531.jpg"  # URL of the input image
image_url = "https://spector-promostandard.s3.amazonaws.com/promostandard-document/1_EC153_v1727288531.jpg"
output_file_path = "output_image.png"  # Where to save the output image
remove_background_from_image(token,image_url, output_file_path)
