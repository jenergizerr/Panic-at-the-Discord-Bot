import requests
import os
import io
import discord
import json
import PIL
from PIL import Image
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv


load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#why would you do anything but !
bot = commands.Bot(command_prefix="!")

#outfit list from the outfits files
outfits = ["uni", "werk", "br", "malluni", "lol", "redhat", "blackhat" ]

#get image from a link instead of DL all
def make_image_url(token_id):

    contract_address = "0x73d6f8a959094e0424802bc8add670f9a790cd1b"
    os_url = "https://api.opensea.io/api/v1/asset/" + contract_address + "/" + str(token_id) + "/?format=json"
    print(os_url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    response = requests.get(os_url, headers=headers)
    metadata = json.loads(response.text)

    pfp_image_url = requests.get(metadata["image_url"])
    pfp_image = Image.open(BytesIO(pfp_image_url.content))
    pfp_image.save("pfp_image.png")

    return pfp_image, pfp_image_url

#make the image collage
def get_dressed(fit, pfp_id):
    #url = (get_pfp_img_url(pfp_id))
    #download_image(url, pfp_folder + str(pfp_id) + '.png')
    # This combines the images
    # pfp = Image.open(pfp_folder + str(pfp_id) + '.png')

    pfp_image, pfp_image_url = make_image_url(pfp_id)
    print("Got the pfp image url:", pfp_image_url)
    outfit = Image.open("outfits/" + fit + '.png')

    pfp_image.paste(outfit, (0, 0), mask=outfit)
    pfp_image.save("pfp_image.png")

    #pfp_image.show()
    #pfp.save(save_img_folder + 'dressed' + str(pfp_id) + '.png')

    return pfp_image

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="apply")
async def apply(ctx, fit: str, pfp_id: int):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 1900:
            pfp_image = get_dressed(fit, str(pfp_id))
            await ctx.send(file=discord.File("pfp_image.png"))
      else:
        await ctx.send('u think u can get a mcds job with that attn to detail? command !<fits> for ways 2 survive the dip')
    except:
        await ctx.send('Please enter a valid number between 1 and 1900.')

# Lists the different "fits" available. This just returns the outfits list on new lines

@bot.command(name="fits", brief='ways 2 survive the dip', description='This command will list the different outfits available to you')
async def fits(ctx):
    await ctx.send('**Command Avails (please choose from one of the below)**\n\n'+ "\n".join(outfits))

# Lets user know when they enter an invalid command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("Unknown command, please check !help for a list of available commands")

bot.run(os.getenv("DISCORD_TOKEN"))
