import requests
import json
from dotenv import load_dotenv
import os
import random

load_dotenv()

class Flux:
    def __init__(self):
        self.api_token = os.getenv("FLUX_API_TOKEN")

    def generate_image(
        self,
        prompt: str,
        model: str = "flux-pro-max",
        width: int = 1024,
        height: int = 768,
        prompt_upsampling: bool = False,
        seed: int = random.randint(0, 2**32 - 1),
        safety_tolerance: int = 5
    ) -> dict:
        """
        Generate an image using the Flux API.
        
        Args:
            api_token (str): Your API token
            prompt (str): The text prompt to generate the image
            model (str, optional): Model name. Defaults to "flux-pro"
            width (int, optional): Image width. Defaults to 1024
            height (int, optional): Image height. Defaults to 768
            prompt_upsampling (bool, optional): Enable prompt upsampling. Defaults to False
            seed (int, optional): Random seed. Defaults to 42
            safety_tolerance (int, optional): Tolerance level for input and output moderation. Between 0 and 6, 0 being most strict, 6 being least strict.
        
        Returns:
            dict: API response
        """
        url = f"https://apis.bltcy.ai/v1/images/generations"
        
        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "size": f"{width}x{height}",
            "model": model,
            "prompt_upsampling": prompt_upsampling,
            "seed": seed,
            "safety_tolerance": safety_tolerance
        }
        
        try:
            response = requests.request("POST", url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json().get("data")[0].get("url")
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    flux = Flux()

    # Example request
    result = flux.generate_image(
        prompt="A captivating woman lounges on a soft, cream-colored chaise, her long, flowing hair framing a face adorned with radiant skin. She wears a minimal lace bralette and matching high-waisted panties, tastefully highlighting her alluring silhouette. One leg is playfully bent, accentuating her toned thigh, while her other foot rests delicately on the ground. Her sultry gaze, paired with a mischievous smile, beckons the viewer closer. The room is dimly lit, with flickering candlelight casting soft shadows that dance across her curves, evoking an atmosphere of intimacy and undeniable temptation, enveloped in a warm, seductive glow.",
    )
    
    if result:
        print(f"Generated image URL: {result}")