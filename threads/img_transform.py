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
    cdn_image_url = "https://delivery-eu1.bfl.ai/results/a2605d8fe8954dc581a87cabacd43815/sample.jpeg?se=2025-01-07T08%3A46%3A02Z&sp=r&sv=2024-11-04&sr=b&rsct=image/jpeg&sig=Y7EYAPPTG6rTICg3GvYb7Rvcf7YRyxMCFiTPfRgV0ss%3D"  # Replace with your CDN URL
    jpg_url = convert_and_get_jpg_url(cdn_image_url)
    print(f"Converted JPG URL: {jpg_url}")
