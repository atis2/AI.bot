import json
import time
import base64
from PIL import Image
from io import BytesIO
import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=60, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
def show(prompt):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'EB9DF08F312BD7134EC9E8B1AA53AB00', 'B57D2C9556A05074ED4E9EEECEC3AF14')
    model_id = api.get_model()
    uuid = api.generate(f"{prompt}", model_id)
    images = api.check_generation(uuid)[0]  
    
    if images.startswith("data:image"):
        images = images.split(",")[1]

    image_data = base64.b64decode(images)
    with open("output_image.png", "wb") as f:
        f.write(image_data)
    return "output_image.png"

if __name__ == '__main__':
    showw = show('car')
#Не забудьте указать именно ваш YOUR_KEY и YOUR_SECRET.