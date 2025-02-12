import websocket
import uuid
import json
import urllib.request
import urllib.parse
import os
import io
import random
from PIL import Image
import time
from datetime import datetime

class GenImg:
    def __init__(self):
        self.client_id = str(uuid.uuid4())
        self.server_address = '127.0.0.1:8188'

    def open_websocket_connection(self):
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        return ws, self.server_address, self.client_id

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt",
            data=data,
            headers=headers
        )
        return json.loads(urllib.request.urlopen(req).read())
    
    def track_progress(self, prompt, ws, prompt_id):

        node_ids = list(prompt.keys())
        finished_nodes = []

        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'progress':
                    data = message['data']
                    current_step = data['value']
                    print('In K-Sampler -> Step: ', current_step, ' of: ', data['max'])
                if message['type'] == 'execution_cached':
                    data = message['data']
                    for itm in data['nodes']:
                        if itm not in finished_nodes:
                            finished_nodes.append(itm)
                            print('Progess: ', len(finished_nodes), '/', len(node_ids), ' Tasks done')
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] not in finished_nodes:
                        finished_nodes.append(data['node'])
                        print('Progess: ', len(finished_nodes), '/', len(node_ids), ' Tasks done')

                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue
        return
    
    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())

    def get_image(self, filename, subfolder, folder_type, server_address):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
            return response.read()

    def get_images(self, prompt_id, allow_preview = False):
        output_images = []

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    output_data = {}
                    if allow_preview and image['type'] == 'temp':
                        preview_data = self.get_image(image['filename'], image['subfolder'], image['type'], self.server_address)
                        output_data['image_data'] = preview_data
                    if image['type'] == 'output':
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'], self.server_address)
                        output_data['image_data'] = image_data
                    output_data['file_name'] = image['filename']
                    output_data['type'] = image['type']
                    output_images.append(output_data)

        return output_images

    def save_image(self, images, output_path, save_previews):
        for itm in images:
            directory = os.path.join(output_path, 'temp/') if itm['type'] == 'temp' and save_previews else output_path
            os.makedirs(directory, exist_ok=True)
            try:
                image = Image.open(io.BytesIO(itm['image_data']))
                image.save(os.path.join(directory, itm['file_name']))
            except Exception as e:
                print(f"Failed to save image {itm['file_name']}: {e}")  

    def load_workflow(self, workflow_path):
        try:
            with open(workflow_path, 'r') as file:
                workflow = json.load(file)
                return json.dumps(workflow)
        except FileNotFoundError:
            print(f"The file {workflow_path} was not found.")
            return None
        except json.JSONDecodeError:
            print(f"The file {workflow_path} contains invalid JSON.")
            return None
    
    def generate_image_by_prompt(self, prompt, output_path, save_previews=False):
        try:
            ws, server_address, self.client_id  = self.open_websocket_connection()
            prompt_id = self.queue_prompt(prompt)['prompt_id']
            self.track_progress(prompt, ws, prompt_id)
            images = self.get_images(prompt_id, save_previews)
            filenames = []
            for image in images:
                filenames.append(image['file_name'])
            print(f"Generated images: {filenames}")
            self.save_image(images, output_path, save_previews)
        finally:        
            ws.close()

        return filenames

if __name__ == "__main__":

    # Initialize the GenImg instance
    gen_img = GenImg()
    
    # Load workflow from file
    workflow_path = os.path.join('threads','workflow', 'yi_ying.json') 
    workflow = gen_img.load_workflow(workflow_path)
    
    if workflow is None:
        print("Failed to load workflow")        
        exit(1)
    prompttext="""
    'IMG_4567.JPG of yi_ying, a young Asian woman, standing in a sunlit garden. She wears a light blue tank top with a scoop neckline, accentuating her curves, paired with high-waisted jeans. Her expression is relaxed, with a soft smile, and her hair flows naturally in the breeze. The warm, natural lighting highlights her casual elegance.'
    """   
    workflowjson = json.loads(workflow)
    print(workflowjson)

    id_to_title = {id: details.get('_meta', {}).get('title', '') for id, details in workflowjson.items()}
    positive_prompt = [key for key, value in id_to_title.items() if value == 'Positive Prompt'][0]
    save_image_node = [key for key, value in id_to_title.items() if value == 'Save Image'][0]
    timestamp = datetime.now().strftime("%y%m%d_%H%M")

    workflowjson.get(positive_prompt)['inputs']['text'] = prompttext
    workflowjson.get(save_image_node)['inputs']['filename_prefix'] = timestamp + '_yi_ying'
    
    # # Example prompts - you can modify these or pass them as arguments
    # positive_prompt = "your positive prompt here"
    # negative_prompt = "your negative prompt here"
    
    # postive_input_id = prompt.get(k_sampler)['inputs']['positive'][0]
    # prompt.get(postive_input_id)['inputs']['text'] = positive_prompt

    # if negative_prompt != '':
    #     negative_input_id = prompt.get(k_sampler)['inputs']['negative'][0]
    #     prompt.get(negative_input_id)['inputs']['text'] = negative_prompt

    gen_img.generate_image_by_prompt(workflowjson, './output/', save_previews=False)