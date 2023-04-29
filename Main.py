import requests
import json
import time
import os


api_key = "6bbb92eb-ab95-4e68-9d35-ffb6348439ae"
model = "anything-v4.5-pruned.ckpt [65745d25]"
#models: (realistic) "deliberate_v2.safetensors [10ec4b29]", (stable Diffusion) "anything-v4.5-pruned.ckpt [65745d25]"

def get_job_code(response_text):
    response_dict = json.loads(response_text)
    job_code = response_dict["job"]
    return job_code

def job_creator(prompt, neg_prompt):
    
    url = "https://api.prodia.com/v1/job"
    payload = {
        "model": model,
        "prompt": prompt,
        "negative_prompt": neg_prompt, 
        "steps": 30,
        "cfg_scale": 7,
        "seed": -1,
        "upscale": True,
        "sampler": "DPM++ 2M Karras",
        "aspect_ratio": "square"
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": api_key
    }

    # Send the request to create the job and retrieve the job code
    post_response = requests.post(url, json=payload, headers=headers)
    output = post_response.text
    job = get_job_code(output)


    # Check the job status until it succeeds or fails
    while True:
        url = "https://api.prodia.com/v1/job/" + job
        response = requests.get(url, headers=headers)
        response_dict = json.loads(response.text)
        job_status = response_dict["status"]
        
        if job_status == "succeeded":
            image_url = response_dict["imageUrl"]
            return image_url
        elif job_status == "failed":
            print("Job failed!")
            return "none"
        else:
            time.sleep(5) # wait for 5 seconds before checking again

def save_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.basename(url)
        path = "D:/Python Projects/WaifuGenerator/output"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/{filename}", "wb") as f:
            f.write(response.content)
            print(f"{filename} saved successfully.")
    else:
        print("Error in saving the image.")

# Read the prompt from prompt.txt
with open("D:\Python Projects\WaifuGenerator\prompts.txt", "r") as f:
    prompts = f.read().splitlines()

# Read the neg_prompt from neg_prompt.txt
with open("D:\\Python Projects\\WaifuGenerator\\neg_prompts.txt", "r") as f:
    neg_prompt = f.readline().strip()

# Generate and save images for each prompt
for prompt in prompts:
    if(prompt == "end"):
        break
    for i in range(4):
        url = job_creator(prompt, neg_prompt)
        save_image(url)