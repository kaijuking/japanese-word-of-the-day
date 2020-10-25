import pytest
import tweepy
from src.tweet import Tweet
from src.word import get_random_word, transform_data_from_database


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


def get_random_word():

    examples = [
        {
            'message': 'Word: test1, Meaning: test1', 
            'timeline': 'Word: word, Meaning: meaning',
            'expected': 'Word: test1, Meaning: test1'
        },
        {
            'message': 'Word: test2, Pronunciation: test2, Meaning: test2',
            'timeline': 'Word: test2, Pronunciation: test2, Meaning: test2',
            'expected': 'Thank you for following MaikuOnline! 毎日頑張りましょう！'
        }
    ]

    for item in examples:
        word_list = []
        timeline_posts = []
        
        word_list.append(item['message'])
        timeline_posts.append(item['timeline'])

        result = get_random_word(word_list, timeline_posts)
        assert result == item['expected']


def get_random_word_invalid_data():

    examples = [
        {'wordList': None, 'timeLinePost': ['Word: word, Meaning: meaning']},
        {'wordList': ['Word: word, Meaning: meaning'], 'timeLinePost': None},
    ]

    for item in examples:
        result = get_random_word(item['wordList'], item['timeLinePost'])
        assert result == 'Error trying to get a random word.'