import discord
import pprint
import secrets
import tweepy
import threading
import logging
import asyncio
import tweets_to_discord_with_streams as tweepy

valid_commands = ['!insertkey', '!removekey', '!display', '!insertname', '!removename']
LOG_FILE_NAME = "user-tweets-to-discord-from-json-file-LOG.txt"
default_keywords = []
default_names = []

client = discord.Client()


async def start():
    loop = asyncio.get_event_loop()
    await loop.create_task(client.start(secrets.discord_bot_token))
    threading.Thread(target=loop.run_forever())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    pprint.pprint(message)
    if message.author == client.user:
        return
    channel = message.channel
    message = message.content
    await handle_message(channel, message)


async def handle_message(channel, message):
    if message.startswith('!hello'):
        logging.info("Hello command triggered")
        await say_hello(channel)
    elif message.startswith('!insertkey'):
        logging.info("Insert key command triggered")
        await insert_key(channel, message)
    elif message.startswith('!removekey'):
        logging.info("Remove key command triggered")
        await remove_key(channel, message)
    elif message.startswith('!display'):
        logging.info("Display command triggered")
        await display(channel)
    elif message.startswith('!insertname'):
        logging.info("Insert name command triggered")
        await insert_name(channel, message)
    elif message.startswith('!removename'):
        logging.info("Remove name command triggered")
        await remove_name(channel, message)


async def say_hello(channel):
    await channel.send('Hello!')


async def insert_key(channel, message):
    new_keywords = message.replace('!', '').split()
    new_keywords.pop(0)
    tweepy.default_keywords.extend(new_keywords)
    tweepy.default_keywords.sort()
    await channel.send(f'Added new keyword(s): {" ".join(new_keywords)}')


async def remove_key(channel, message):
    twitter_keys_to_remove = message.replace('!', '').split()
    twitter_keys_to_remove.pop(0)
    tweepy.default_keywords = [key for key in tweepy.default_keywords if key not in twitter_keys_to_remove]
    tweepy.default_keywords.sort()
    await channel.send(f'Removed twitter keyword(s): {" ".join(twitter_keys_to_remove)}')


async def display(channel):
    await channel.send(
        f'Twitter Account Name(s): {" ".join(tweepy.default_names)}\nKeyword(s): {" ".join(tweepy.default_keywords)}')


async def insert_name(channel, message):
    new_twitter_names = message.replace('!', '').split()
    new_twitter_names.pop(0)
    tweepy.default_names.extend(new_twitter_names)
    tweepy.default_names.sort()
    await channel.send(f'Added new twitter name(s): {" ".join(new_twitter_names)}')


async def remove_name(channel, message):
    twitter_names_to_remove = message.replace('!', '').split()
    twitter_names_to_remove.pop(0)
    tweepy.default_names = [name for name in tweepy.default_names if name not in twitter_names_to_remove]
    tweepy.default_names.sort()
    await channel.send(f'Removed twitter name(s): {" ".join(twitter_names_to_remove)}')


client.run(secrets.discord_bot_token)
