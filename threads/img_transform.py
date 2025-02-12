import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv  
import os

load_dotenv()

def convert_and_get_jpg_url(image_url):
    # Configure your Cloudinary account
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    response = cloudinary.uploader.upload(image_url, format="jpg")
    return response['secure_url']  # Returns the URL of the converted JPG image

if __name__ == "__main__":
    # Example usage
    cdn_image_url = "output/250211_1920_yi_ying_00002_.png"  # Replace with your CDN URL
    jpg_url = convert_and_get_jpg_url(cdn_image_url)
    print(f"Converted JPG URL: {jpg_url}")
