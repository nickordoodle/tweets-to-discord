from tweepy import OAuthHandler
import secrets
from classes import *
import tweepy
import json
import sys
from discord import Webhook, RequestsWebhookAdapter


LOG_FILE_NAME = "user-tweets-to-discord-from-json-file-LOG.txt"
default_keywords = []
default_names = []


def log_error_to_file(file_name, err):
    # Appending to file
    with open(file_name, 'a') as log_file:
        log_file.write(err)


def main():
    # Set up authentication for twitter
    auth = OAuthHandler(secrets.twitter_consumer_key, secrets.twitter_consumer_secret)
    auth.set_access_token(secrets.twitter_access_token, secrets.twitter_secret_token)
    # Create the API object itself using authentication
    # Waits on rate limit if it goes over or tries to
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    with open('parameters.json') as params_file:
        json_twitter_settings = json.load(params_file)
        if len(json_twitter_settings) == 0:
            err_msg = "[ERROR] No json data provided"
            log_error_to_file(LOG_FILE_NAME, err_msg)
            print(err_msg)
            sys.exit(0)

    # Create a list to keep track of twitter accounts
    account_list = []
    # Iterate each username and create objects for local usage
    for user_name in json_twitter_settings["default_names"]:
        user_id = api.get_user(screen_name=user_name)
        user_obj = UserAccount(user_name, str(user_id.id), "", "")
        print(user_obj.id)
        # Add to working account list to keep track
        account_list.append(user_obj)

    # Create a simple discord webhook for simple message sending
    discord_webhook = Webhook.from_url(secrets.discord_bot_test_hook, adapter=RequestsWebhookAdapter())
    # Create listener and pass hook and our accounts to watch
    my_stream_listener = MyStreamListener(discord_webhook, account_list)
    # Create the stream itself and set authentication and the listener
    my_stream = tweepy.Stream(auth=auth, listener=my_stream_listener)

    # Flatten ids to get list of all ids
    all_ids = list(map(lambda user: user.id, account_list))
    # One function to start streaming all twitter ids specified by follow
    my_stream.filter(follow=all_ids, is_async=True)


if __name__ == '__main__':
    main()
