import os
from gpt4free import theb
import aiohttp
import discord
from collections import deque
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is running")

def generate_response(prompt):
    response = ""
    while not response:
        for token in theb.Completion.create(prompt):
            response += token
    return response


conversation_history = deque(maxlen=2)

@bot.tree.command(name="gpt", description="Chatbot made using the gpt4free API!")
async def image(interaction: discord.Interaction, *, text: str):



    await interaction.response.send_message(f"**Thinking...**")


    if interaction.message:
        await bot.process_commands(interaction.message)


    global conversation_history

    if interaction.user.bot:

        return 

    if interaction.guild and isinstance(interaction.guild.get_channel(interaction.channel_id), discord.TextChannel):

        conversation_history.append(f"{interaction.user.name}: {interaction.content}")




        prompt = '\n'.join(conversation_history) + f"\nLLM:"
        response = generate_response(prompt)

        conversation_history.append(f"LLM : {response}")

        await interaction.followup.send(response)





bot.run(TOKEN)
