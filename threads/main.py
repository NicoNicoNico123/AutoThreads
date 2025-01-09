from .chain import ChainPrompt
from .serapi import SerpAPI
from .flux import Flux
from .img_transform import convert_and_get_jpg_url
import logging
logging.basicConfig(level=logging.INFO)
from .threads import Threads

class Main:

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
    Main().generate_thread(text="Hello, Threads!")
