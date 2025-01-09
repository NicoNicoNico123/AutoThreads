import yaml
import os
def load_prompt_text(prompt,type):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'prompt', f'{type}.yaml')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_content = yaml.safe_load(file)
            
        if prompt in yaml_content:
            return yaml_content[prompt]
        else:
            print(f"Error: '{prompt}' key not found in the YAML file.")
            return None
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None