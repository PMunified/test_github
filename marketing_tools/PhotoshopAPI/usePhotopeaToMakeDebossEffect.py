import requests
import json
import time

# Set up the Photopea URL
photopea_url = "https://www.photopea.com/api/"

# Function to send command to Photopea
def send_command(cmd, params):
    payload = {
        "cmd": cmd,
        "params": params
    }
    headers = {
    "Content-Type": "application/json"
}
    response = requests.post(photopea_url, json=payload,headers=headers)
    #print(response.status_code)
    #print(response.headers.get('Content-Type', ''))
    return response.json()
    #return response.status_code

# Function to open an image
def open_image(image_url):
    return send_command("open", {"url": image_url})

# Function to create a deboss effect
def create_deboss_effect():
    # Here we simulate debossing with a drop shadow and blurred layers
    # 1. Select the active layer
    send_command("setActiveLayer", {"layer": "1"})  # Change "1" to the layer number you want to modify
    
    # 2. Apply a drop shadow for a deboss effect
    drop_shadow_params = {
        "distance": 5,
        "angle": 120,
        "color": "#000000",
        "opacity": 0.5,
        "blur": 10
    }
    send_command("dropShadow", drop_shadow_params)

    # 3. Optionally apply some other effects or adjustments if needed
    # For example, you could apply a blur to further refine the effect
    send_command("blur", {"radius": 2})

# Function to save the edited image
def save_image(filename):
    return send_command("save", {"name": filename, "format": "png"})  # Specify desired format

# Main Execution
if __name__ == "__main__":
    # Open an image
    image_url = "https://www.spectorandco.com/product_images/products/1_G1254_BLU_OP2__Other_Product_Image_v1_1580942512.jpg"  # Replace with your image URL
    open_response = open_image(image_url)
    print("Open Response:", open_response)

    # Wait for the image to be fully loaded before applying effects
    time.sleep(5)  # Adjust timing as needed based on image size

    # Create the deboss effect
    create_deboss_effect()

    # Save the edited image
    save_response = save_image("debossed_image.png")
    print("Save Response:", save_response)
