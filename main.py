import discord 
import os

from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # OPENAI API KEY
)
token = os.getenv("SECRET_KEY")    # Discord BOT API KEY

chat = ""

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}\n"
        print(f'Message from {message.author}: {message.content}')
        client = OpenAI()  
        if self.user != message.author:
            if self.user in message.mentions:
                response = client.completions.create(
                    model="text-davinci-003",
                    prompt=f"{chat}\nHR_AI_GPT: ",
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                channel = message.channel
                message_to_send = response['choices'][0]['text']
                await channel.send(message_to_send)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
