import tweepy


class UserAccount:
  def __init__(self, user_handle, id, keywords, last_tweet):
    self.user_handle = user_handle
    self.id = id
    self.keywords = keywords
    self.last_tweet = last_tweet

  def check_user_timeline(self, new_timeline):
    pass

  def get_keywords(self):
    return self.keywords

  def print_params(self):
    print("user_handle: " + self.user_handle)
    print("keywords: " + self.keywords)
    print("last tweet: " + self.last_tweet)

# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    """
    Twitter listener, collects streaming tweets and output to a file
    """

    def __init__(self, discord_hook, account_list):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("log_file.txt", "w")
        self.discord_hook = discord_hook
        self.account_list = account_list

    def on_status(self, status):
        new_tweet = status.text
        print(new_tweet)
        if status.retweeted is False and "RT" not in new_tweet[:2]:
            self.discord_hook.send(new_tweet)
            # get user id
            #TODO Check tweets against keywords

        # Stops streaming when it reaches the limit
        if self.num_tweets <= 1000:
            if self.num_tweets % 100 == 0:  # just to see some progress...
                print('Number of tweets captured so far: {}'.format(self.num_tweets))
            return True
        else:
            return False
        self.file.close()

    def get_user(self, id, account_list):
        for user_obj in account_list:
            if user_obj.id == id:
                return user_obj

    def on_error(self, status):
        print(status)