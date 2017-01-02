import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'qAhZWyyxyi8MQZwxaCKojiC8O'
consumer_secret = 'vCvQvS8icQpNucs5e42JZ0YqdmZkFg6QeGE3PH1sSUeZYyKzvC'
access_token = '2892604311-sLujj8H3JB5oHbIVPGZhC2vkZYNbW3CJsh2LICs'
access_secret = '9MFpHT1HKFmMyf3XD1UzH8APE0QwpkgbDEqt95GHmWQcw'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('americas_tweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            return True

        def on_error(self, status):
            print(status)
            return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(locations=[-173, -56.9, -29.7, 71.1])

