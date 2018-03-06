from tweepy import OAuthHandler
import tweepy
import urllib3
from textblob import TextBlob

urllib3.disable_warnings()


class Twitter:

    fetched_tweets = []
    tweet_sentiment_list = []
    obj_api = None
    number_of_tweets = 0
    number_of_positive_tweets = 0
    number_of_negative_tweets = 0
    number_of_neutral_tweets = 0

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

    def authenticate(self):
        authenticator = OAuthHandler(self.consumer_key, self.consumer_secret)
        authenticator.set_access_token(self.access_token, self.access_secret)
        self.obj_api = tweepy.API(authenticator)

    def fetch_tweets(self, query, number):
        self.fetched_tweets = self.obj_api.search(q=query, count=number)
        return self.fetched_tweets

    def find_sentiment(self):
        if len(self.fetched_tweets) is 0:
            return

        for tweet in self.fetched_tweets:
            tweet_polarity = TextBlob(tweet.text).polarity
            if tweet.retweet_count > 0:
                if tweet not in self.tweet_sentiment_list:
                    self.tweet_sentiment_list.append({tweet.text: tweet_polarity})
            else:
                self.tweet_sentiment_list.append({tweet.text: tweet_polarity})

            self.number_of_tweets += 1

            if tweet_polarity > 0:
                self.number_of_positive_tweets += 1
            elif tweet_polarity < 0:
                self.number_of_negative_tweets += 1
            else:
                self.number_of_neutral_tweets += 1

        return self.tweet_sentiment_list

    def positive_tweet_percentage(self):
        if self.number_of_tweets == 0:
            return None

        return (100 * self.number_of_positive_tweets) / self.number_of_tweets

    def negative_tweet_percentage(self):
        if self.number_of_tweets == 0:
            return None

        return (100 * self.number_of_negative_tweets) / self.number_of_tweets

    def neutral_tweet_percentage(self):
        if self.number_of_tweets == 0:
            return None

        return (100 * self.number_of_neutral_tweets) / self.number_of_tweets


consumerkey = ''
consumersecret = ''
accesstoken = ''
accesssecret = ''

twitter = Twitter(consumerkey, consumersecret, accesstoken, accesssecret)
twitter.authenticate()
fetched_tweets = twitter.fetch_tweets("Thor Ragnarok", 100)
twitter.find_sentiment()


print 'Positive: ', twitter.positive_tweet_percentage(), '%'
print 'Negative: ', twitter.negative_tweet_percentage(), '%'
print 'Neutral: ', twitter.neutral_tweet_percentage(), '%'

