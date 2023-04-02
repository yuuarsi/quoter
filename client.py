import discord
from html_renderer import render, QUOTE_SAVE_PATH
from config import CONFIGS as cfg
import random

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        if cfg['RandomReply']['Enable']:
            try:
                self.store_channel = client.get_channel(cfg['RandomReply']['StoreChannel'])
                self.text_channel = client.get_channel(cfg['RandomReply']['ReplyChannel'])
                self.quotes_cache = {m.id: m async for m in self.store_channel.history(limit=None)}
                self.message_counter = 0
                self.reply_trigger = random.randint(cfg['RandomReply']['ReplyTrigger'], cfg['RandomReply']['ReplyTrigger'] + 50)
            except:
                cfg['RandomReply']['Enable'] = False

    async def on_message(self, message: discord.Message):
        if not message.guild:
            return
        if message.author.bot:
            return
        
        if cfg['RandomReply']['Enable']:
            if message.channel.id == cfg['RandomReply']['ReplyChannel']:
                self.message_counter += 1
                if self.message_counter >= self.reply_trigger:
                    self.message_counter = 0
                    self.reply_trigger = random.randint(cfg['RandomReply']['ReplyTrigger'], cfg['RandomReply']['ReplyTrigger'] + 50)
                    if len(self.quotes_cache) < 10:
                        return

                    quote_list = sorted(QUOTE_SAVE_PATH.glob('*.png'))
                    await message.reply(file=discord.File(random.choice(quote_list)))

        if not client.user.mentioned_in(message):
            return

        if message.reference is not None:
            quote_msg = message.reference.resolved
            if quote_msg is discord.DeletedReferencedMessage or quote_msg is None:
                return
            
            content = quote_msg.clean_content
            if content == "":
                return

            author = quote_msg.author

            async with message.channel.typing():
                img, id = render(author.name, author.discriminator, author.display_name, content, author.display_avatar.url)
                await message.reply(file=discord.File(img, filename=f"{id}.png"))
                if cfg['RandomReply']['Enable']:
                    sent = await self.store_channel.send(f'ID: {id}\nContent: {content}\nAuthor: {author.mention}\nCreator: {message.author.mention}')
                    self.quotes_cache[sent.id] = sent

    async def on_raw_message_delete(self, payload):
        if cfg['RandomReply']['Enable']:
            if payload.channel_id == cfg['RandomReply']['StoreChannel']:
                deleted = self.quotes_cache.get(payload.message_id)
                id = deleted.content.split('\n')[0][4:]
                del self.quotes_cache[payload.message_id]
                img_to_del = QUOTE_SAVE_PATH / (id + '.png')
                img_to_del.unlink(missing_ok=True)

intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.messages = True

client = MyClient(intents=intents)
client.allowed_mentions = discord.AllowedMentions.none()
client.allowed_mentions.replied_user = True

client.run(cfg['Token'])