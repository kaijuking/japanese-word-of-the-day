import pytest
import tweepy
from src.tweet import Tweet


def test_default_post():
    access_keys = ''
    new_tweet = Tweet(access_keys)
    result = new_tweet.get_default_post()
    assert result == "Thank you for following MaikuOnline! 毎日頑張りましょう！"


def test_get_last_post_inavlid_creds():
    access_keys = {
                'TWEEPY_CONSUMER_KEY': None, 
                'TWEEPY_CONSUMER_SECRET': None, 
                'TWEEPY_ACCESS_TOKEN': None, 
                'TWEEPY_ACCESS_TOKEN_SECRET': None
            
        }
    new_tweet = Tweet(access_keys)
    result = new_tweet.get_last_post()
    assert result.response is None


def test_get_last_post_inavlid_creds2():
    access_keys = {
                'TWEEPY_CONSUMER_KEY': 'None', 
                'TWEEPY_CONSUMER_SECRET': 'None', 
                'TWEEPY_ACCESS_TOKEN': 'None', 
                'TWEEPY_ACCESS_TOKEN_SECRET': 'None'
            
        }
    new_tweet = Tweet(access_keys)
    result = new_tweet.get_last_post()
    assert result.args[0][0]['code'] == 89
    assert result.args[0][0]['message'] == 'Invalid or expired token.'