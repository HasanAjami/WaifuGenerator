import requests
import json
import time
import os
import random
import discord
from discord.ext import commands

import sys

last_saved_prompt = "x"
last_saved_model = "x"
saved_image_name = 'generated_image.png'

prompt_src = ["D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Background.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Body.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\BreastsToModify.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\ClothesToModify.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Expression.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\EyesToModify.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Hair.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\HairColorToModify.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\HairLengthToModify.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\HairStuff1.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Hands.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Head.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Legs.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Legwear2.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\MouthToModify.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Other.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Panties.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Posture1.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Posture2.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Sleeves.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\StyleOfHair.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody1.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody2.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody3.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody4.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody5.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody6.txt",
              "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\UpperBody7.txt"]

prompt_clothes_src = "D:\\Python Projects\\WaifuGenerator\\auto_prompts\\Clothes"


#Discord intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)
#shows a list of commands
@bot.command()
async def commands(ctx):
    await ctx.send("Hi! I am Hasan's Waifu, I'm the mommy of his creations! \n You can use me to generate waifus and do other stuff, here are my commands: \n !newWaifu to generate a Waifu, I will then ask for a model (choose number), you then type the prompt or random for a random prompt! \n !saveImage to save in generations_showcase \n !redo to redo the previous prompt, if the Waifu looked like shit \n !tellElyasJoke to tell Elyas a stupid joke! \n happy to hear from you :D")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello! {ctx.author}')

@bot.command()
async def bye(ctx):
    await ctx.send('Finally! Get some bitches! byeeeee...')
#shuts the bot down
@bot.command()
async def killYourSelf(ctx):
    await ctx.send("OK I go die")
    sys.exit()

@bot.command()
async def thank_you(ctx):
    await ctx.send("No problem! Always happy to help")
    sys.exit()



#------------------------------------------------------------------------------------------------------------------
#'Prodia API'
api_key = "6bbb92eb-ab95-4e68-9d35-ffb6348439ae"
model = "meinamix_meinaV9.safetensors [2ec66ab0]"



#Prodia AI GET and POST:
#GET
def get_job_code(response_text):
    response_dict = json.loads(response_text)
    job_code = response_dict["job"]
    return job_code
#POST
def job_creator(prompt, neg_prompt, job_model): 

    
    url = "https://api.prodia.com/v1/job"
    payload = {
        "model": job_model,
        "prompt": prompt,
        "negative_prompt": neg_prompt, 
        "steps": 40,
        "cfg_scale": 8,
        "seed": -1,
        "upscale": True,
        "sampler": "Euler a", #Euler a, DPM++ 2M Karras
        "aspect_ratio": "square"
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": api_key
    }

    #post request, Send the request to create the job and retrieve the job code
    post_response = requests.post(url, json=payload, headers=headers)
    output = post_response.text
    job = get_job_code(output)


    #get request, Check the job status until it succeeds or fails
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
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Waifu Generating commands

def get_random_text_from_clothes_folder():
    clothes_folder_path = prompt_clothes_src  # Replace this with the path to your "clothes" folder

    # Get a list of all folders inside the "clothes" folder
    subfolders = [f.name for f in os.scandir(clothes_folder_path) if f.is_dir()]

    if not subfolders:
        print("No folders found inside 'clothes' folder.")
        return None

    # Select a random folder from the list
    selected_folder = random.choice(subfolders)

    folder_path = os.path.join(clothes_folder_path, selected_folder)

    # Get a list of all text files inside the selected folder
    text_files = [f.name for f in os.scandir(folder_path) if f.is_file() and f.name.endswith(".txt")]

    if not text_files:
        print(f"No text files found inside '{selected_folder}' folder.")
        return None

    # Select a random text file from the list
    selected_textfile = random.choice(text_files)

    textfile_path = os.path.join(folder_path, selected_textfile)

    # Read the text inside the selected text file
    with open(textfile_path, "r") as file:
        text_content = file.read()

    return text_content


def random_prompt_gen():
    output_prompt = ""
    for file_path in prompt_src:
        with open(file_path, "r") as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            element = random_line.strip().lstrip("- ") # remove leading hyphen and any spaces after it
            output_prompt += element + ", "
    return output_prompt.rstrip(", ")

@bot.command()
async def random_prompt(ctx):
    rand_res =  random_prompt_gen()

    await ctx.send("Your random prompt: " + rand_res)

@bot.command()
async def newWaifu(ctx, amount = 0):
    amount = int(amount)
    if(amount > 0): amount -= 1
    
    change_random = False
    job_author = ctx.author
    mention = job_author.mention
    # Send a message to the channel asking for a prompt
   # get user's prompt
    await ctx.send("Which model do you want to use? please choose from: \n 1: delibrate \n 2: meina \n 3: anything \n 4: realistic")
    prompt = await bot.wait_for('message', check= lambda m: m.author == ctx.author)
    prompt = prompt.content
    my_model = "meinamix_meinaV9.safetensors [2ec66ab0]"
    match prompt:
        case "1":
            my_model = "deliberate_v2.safetensors [10ec4b29]"
            await ctx.send("Ok changed to delibrate")
        case "2":
            my_model = "meinamix_meinaV9.safetensors [2ec66ab0]"
            await ctx.send("Ok changed to meinaMix")
        case "3":
            my_model = "anything-v4.5-pruned.ckpt [65745d25]"
            await ctx.send("Ok changed to anything v5")
        case "4":
            my_model = "shoninsBeautiful_v10.safetensors [25d8c546]"
            await ctx.send("Ok changed to shonin (realistic)")
        case default:
            await ctx.send("That was not a valid model, will use meina")


    await ctx.send("What do you want your waifu to look like?")
    prompt = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    prompt = prompt.content

    if(prompt == "random"):
        change_random = True
    elif(prompt == "stop" or prompt == "cancle" or prompt == "exit"):
        return
        


    while(amount >= 0):
        if(change_random == True):
            prompt = random_prompt_gen() + ", " + get_random_text_from_clothes_folder()
            await ctx.send("Next job prompt is: " + prompt)
        await ctx.send(f"Generating... {amount} job(s) left")
        global last_saved_prompt
        global last_saved_model
        last_saved_model = my_model
        last_saved_prompt = prompt
        # generate the image using the prompt
        url = job_creator(prompt, "bad anatomy, inaccurate eyes, bad quality", my_model)
    
        # download the image and save it as a file
        response = requests.get(url)
        with open(saved_image_name, 'wb') as f:
            f.write(response.content)
        
        # send the image to the channel
        with open(saved_image_name, 'rb') as f:
            await ctx.send(file=discord.File(f, saved_image_name))
        amount -= 1
    
    await ctx.send(f"Alright, no jobs left! Remember to say thank you {mention} >:3 ")

@bot.command()
async def saveImage(ctx,  *, message_id: str):
    message_id = [int(num.strip()) for num in message_id.split(',')]
    for my_id in message_id:
        message = await ctx.fetch_message(my_id)
        image_url = None
        
        for attachment in message.attachments:
            if attachment.width:
                image_url = attachment.url
                break
        
        if not image_url:
            await ctx.send("No image found in the specified message.")
            return

        channel = bot.get_channel(1099661736224751657) # replace with the destination channel ID
        await channel.send(image_url)

@bot.command()
async def redo(ctx, additional = " "):
    if(last_saved_prompt != "x" and last_saved_model != "x"):
        
        await ctx.send("I will redo: " + last_saved_prompt + ", " + additional)
        
        url = job_creator(last_saved_prompt  + ", " + additional, "bad anatomy, inaccurate eyes, bad quality", last_saved_model)
    
    # download the image and save it as a file
        response = requests.get(url)
        with open(saved_image_name, 'wb') as f:
            f.write(response.content)
    
    # send the image to the channel
        with open(saved_image_name, 'rb') as f:
            await ctx.send(file=discord.File(f, saved_image_name))

    else:
        await ctx.send("Sorry, I wasn't called before! Please use !newWaifu")

IMAGE_SAVE_PATH = r"D:\Apps\Unity\My project\Assets\CardPrefab\StatsSource\Waifus"


def get_last_saved_number():
    files = os.listdir(IMAGE_SAVE_PATH)
    if not files:
        return 0

    numbers = [int(filename.split('.')[0]) for filename in files if filename.isdigit()]
    if not numbers:
        return 0

    return max(numbers)



token = "MTEwMzc3OTAyMzU0NjQ4Mjc4OQ.GUBObm.5eS8WnFznUX3zaTGV2oJWOqSVA5WbBW9jBJ920"
#client.run(token)
bot.run(token)





