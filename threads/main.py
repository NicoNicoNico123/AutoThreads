from .chain import ChainPrompt
from .serapi import SerpAPI
from .flux import Flux
from .img_transform import convert_and_get_jpg_url
import logging
from .comfy_api import GenImg
logging.basicConfig(level=logging.INFO)
from .threads import Threads
import time
import os
import json
from datetime import datetime

class Main:

    def local_thread(self):

        max_retries = 3

        for attempt in range(max_retries):
            try:
                prompttext = ChainPrompt().flux_prompt()
                logging.info(f"Flux prompt: {prompttext}")
                # Setup workflow (only once)
                gen_img = GenImg()
                workflow_path = os.path.join('threads','workflow', 'yi_ying.json') 
                workflow = gen_img.load_workflow(workflow_path)      

                if workflow is None:
                    logging.error("Failed to load workflow")        
                    return None
                
                workflowjson = json.loads(workflow)
                id_to_title = {id: details.get('_meta', {}).get('title', '') for id, details in workflowjson.items()}
                positive_prompt = [key for key, value in id_to_title.items() if value == 'Positive Prompt'][0]
                save_image_node = [key for key, value in id_to_title.items() if value == 'Save Image'][0]

                # Set up generation parameters
                timestamp = datetime.now().strftime("%y%m%d_%H%M")
                workflowjson.get(positive_prompt)['inputs']['text'] = prompttext
                workflowjson.get(save_image_node)['inputs']['filename_prefix'] = timestamp + '_yi_ying'

                # Generate and post images
                images_name = gen_img.generate_image_by_prompt(workflowjson, './output/', save_previews=False)
                logging.info(f"Generated images: {images_name}")

                for image_name in images_name:
                    image_url = convert_and_get_jpg_url("output/" + image_name)
                    logging.info(f"Final image URL: {image_url}")
                    creation_id = Threads().post_thread(text="", image_url=image_url)
                    logging.info(f"Thread creation_id created: {creation_id}")
                    if not creation_id:
                        raise ValueError(f"Failed to post thread for image: {image_name}")
                    print("Thread posted successfully:", creation_id)

                return True  # Return True on successful completion

            except Exception as e:
                logging.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    sleep_time = (2 ** attempt) * 2  # Exponential backoff: 2, 4, 8 seconds
                    logging.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logging.error("All retry attempts exhausted")
        
        return None  # Return None if all retries failed

    def generate_thread(self, text: str):
        
        flux_prompt = ChainPrompt().flux_prompt()
        logging.info(f"Flux prompt: {flux_prompt}")

        # Try up to 3 times with exponential backoff
        max_retries = 3

        for attempt in range(max_retries):
            try:
                raw_url = Flux().generate_image(flux_prompt)
                if raw_url:
                    logging.info(f"Generated image URL: {raw_url}")

                else:
                    logging.warning(f"Attempt {attempt + 1}/{max_retries} failed: No URL returned")
            except Exception as e:
                logging.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    sleep_time = (2 ** attempt) * 2  # Exponential backoff: 2, 4, 8 seconds
                    logging.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                continue
        if not raw_url:
            logging.error("All attempts failed to generate image")
            return None

        image_url = convert_and_get_jpg_url(raw_url)
        logging.info(f"Final image URL: {image_url}")
        creation_id = Threads().post_thread(text=text, image_url=image_url)
        logging.info(f"Thread creation_id created: {creation_id}")
        if creation_id:
            print("Thread posted successfully:", creation_id)
        else:
            print("Failed to post thread")

    # result = SerpAPI().main()
    # # result = SerpAPI().main()
    # output = interact_chain(result)
    # Threads().main(output)

if __name__ == "__main__":
    try:
        main = Main()
        main.local_thread()
    except Exception as e:
        logging.error(f"Error running main: {str(e)}")
