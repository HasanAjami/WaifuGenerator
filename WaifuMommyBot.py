import requests
import json
import time
import os
import random
import discord
from discord.ext import commands

last_saved_prompt = "x"
last_saved_model = "x"

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

elyas_jokes = [
    "Why did Elyas bring a ladder to the party? He heard the drinks were on the house!",
    "What did Elyas say when he found a job as a professional window washer? 'I'm finally seeing things clearly!'",
    "Why did Elyas take up yoga? To find his inner peace and quiet his mind, but mostly because he wanted to touch his toes without feeling winded.",
    "Why did Elyas quit his job at the orange juice factory? He just couldn't concentrate!",
    "What do you get when you cross Elyas and a couch? A lounge lizard!",
    "How does Elyas keep his feet warm in the winter? By wearing toe-sts!",
    "What do you call Elyas when he's running late? Delayed, but not defeated!",
    "Why did Elyas go to the bank wearing a mask? He wanted to make a face deposit!",
    "What did Elyas say when he won the marathon? 'I'm running on adrenaline, and also because I don't know where the finish line is!'",
    "How does Elyas like his eggs? With a side of jokes!",
    "Why did Elyas go to the dentist? To get a Bluetooth!",
    "Why did Elyas bring his piano to the beach? He wanted to play some beach-tunes!",
    "What did Elyas say when he got a ticket for speeding? 'I was just trying to get to the punchline faster!'",
    "How does Elyas get his exercise? By running from his problems!",
    "Why did Elyas take a job at the calendar factory? He heard they needed someone who could work months on end!",
    "What do you get when you cross Elyas with a snowman? Frostbite!",
    "Why did Elyas buy a boat? He wanted to sail into the sunset and see what's on the horizon!",
    "What did Elyas say when he went to the barbershop? 'Just a little off the top, and a lot off the sides!'",
    "How does Elyas like his coffee? Strong enough to wake the dead!",
    "Why did Elyas wear a sweater to the zoo? He heard the lion had a mane attraction!",
    "What did Elyas say when he got a new job as a historian? 'I'm looking forward to making history, and then reading about it later!'",
    "How does Elyas stay cool in the summer? By keeping his fans close and his jokes even closer!",
    "Why did Elyas become a comedian? Because he didn't get the memo that puns were bad!",
    "What did Elyas say when he saw a mirror for the first time? 'I look exactly like my reflection!'",
    "How does Elyas like his steak cooked? With a side of medium-rare humor!",
    "Why did Elyas go to the library? He wanted to check out some books and check-in with his literary side!",
    "What did Elyas say when he found a genie in a bottle? 'I wish I had more wishes, but I don't want to be greedy... so I'll take two!'",
    "Why did Elyas bring a parachute to the party? He wanted to make a grand entrance!",
    "How does Elyas like his pizza? With extra cheese, and a lot of saucy puns on the side!",
    "What did Elyas say when he got lost in the woods? \"I am stumped!\" "]





intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def commands(ctx):
    await ctx.send("Hi! I am Hasan's Waifu, I'm the mommy of his creations! \n You can use me to generate waifus and do other stuff, here are my commands: \n !newWaifu to generate a Waifu, I will then ask for a model (choose number), you then type the prompt or random for a random prompt! \n !saveImage to save in generations_showcase \n !redo to redo the previous prompt, if the Waifu looked like shit \n !tellElyasJoke to tell Elyas a stupid joke! \n happy to hear from you :D")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello! {ctx.author}')

@bot.command()
async def bye(ctx):
    await ctx.send('Finally! Get some bitches! byeeeee...')

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
async def tellElyasJoke(ctx):
    edgy_member = discord.utils.get(ctx.guild.members, name='EdgyGamer')
    await ctx.send(f"Hey {edgy_member.mention} here is a joke: " + elyas_jokes[random.randint(0, len(elyas_jokes))])

@bot.command()
async def saveImage(ctx, message_id: int):
    message = await ctx.fetch_message(message_id)
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

#------------------------------------------------------------------------------------------------------------------

api_key = "6bbb92eb-ab95-4e68-9d35-ffb6348439ae"
model = "meinamix_meinaV9.safetensors [2ec66ab0]"




def get_job_code(response_text):
    response_dict = json.loads(response_text)
    job_code = response_dict["job"]
    return job_code

def job_creator(prompt, neg_prompt, job_model): 
    
    url = "https://api.prodia.com/v1/job"
    payload = {
        "model": job_model,
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

@bot.command()
async def newWaifu(ctx):
    # Send a message to the channel asking for a prompt
   # get user's prompt
    await ctx.send("Which model do you want to use? please choose from: \n 1: delibrate \n 2: meina \n 3: anything \n 4: eldreth")
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
            await ctx.send("Ok changed to anything v4.5")
        case "4":
            my_model = "elldreths-vivid-mix.safetensors [342d9d26]"
            await ctx.send("Ok changed to eldreth")
        case default:
            await ctx.send("That was not a valid model, will use meina")


    await ctx.send("What do you want your waifu to look like?")
    prompt = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    prompt = prompt.content

    if(prompt == "random"):
        prompt = random_prompt_gen()
        await ctx.send("Ok, will gen a Waifu for you with the random prompt: " + prompt)

    
    global last_saved_prompt
    global last_saved_model
    last_saved_model = my_model
    last_saved_prompt = prompt
    # generate the image using the prompt
    url = job_creator(prompt, "bad anatomy, inaccurate eyes, bad quality", my_model)
    
    # download the image and save it as a file
    response = requests.get(url)
    with open('generated_image.png', 'wb') as f:
        f.write(response.content)
    
    # send the image to the channel
    with open('generated_image.png', 'rb') as f:
        await ctx.send(file=discord.File(f, 'generated_image.png'))


@bot.command()
async def redo(ctx, additional = " "):
    if(last_saved_prompt != "x" and last_saved_model != "x"):
        
        await ctx.send("I will redo: " + last_saved_prompt + ", " + additional)
        
        url = job_creator(last_saved_prompt  + ", " + additional, "bad anatomy, inaccurate eyes, bad quality", last_saved_model)
    
    # download the image and save it as a file
        response = requests.get(url)
        with open('generated_image.png', 'wb') as f:
            f.write(response.content)
    
    # send the image to the channel
        with open('generated_image.png', 'rb') as f:
            await ctx.send(file=discord.File(f, 'generated_image.png'))

    else:
        await ctx.send("Sorry, I wasn't called before! Please use !newWaifu")




token = "MTEwMzc3OTAyMzU0NjQ4Mjc4OQ.GUBObm.5eS8WnFznUX3zaTGV2oJWOqSVA5WbBW9jBJ920"
#client.run(token)
bot.run(token)





