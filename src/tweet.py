import tweepy
import random


class Tweet:
    def __init__(self, access_keys):
        print('initializing new Tweet object')
        self.access_keys = access_keys
        self.api = self.authenticate_to_account()
        

    def get_default_post(self):
        default_post = [
            "Thank you for following MaikuOnline! #Japanese #日本語",
            "Visit @JapanEverydayJP (https://japaneveryday.jp/) for more about Japanese language, daily life experiences, and cultural literacy! #Japanese #日本語 #文化 #日常生活"
        ]
        return random.choice(default_post)


    def create_new_post(self, message):
        print('Attempting to post a new message...')
        try:
            response = self.api.update_status(message)
            return response
        except tweepy.TweepError as error:
            message = f'Error attempting to post to account. Error = {error}'
            print(message)
            return error

    
    def get_last_post(self):
        print('Attempting to get last post...')
        try:
            last_tweet = self.api.home_timeline()
            return last_tweet[0].text
        except tweepy.TweepError as error:
            message = f'Error attempting to get last post. Error = {error}'
            print(message)
            return error


    def get_last_twenty_posts(self):
        '''
            Per documentation: 
            Returns the 20 most recent statuses posted from the authenticating user or the user specified. It’s also possible to request another user’s timeline via the id parameter.
        '''
        print('Attempting to get user timeline...')
        timeline_posts = []
        try:
            user_timeline = self.api.home_timeline()
            for item in user_timeline:
                timeline_posts.append(item.text)
            return timeline_posts
        except tweepy.TweepError as error:
            message = f'Error attempting to get user timeline. Error = {error}'
            print(message)
            return error

    
    def get_user_info(self):
        '''
            Per documentation: 
            Returns the authenticated user info..
        '''
        print('Attempting to get user info...')
        try:
            user = self.api.me()
            user_info = {
                'user_id': user.id_str,
                'user_name': user.screen_name,
                'description': user.description
            }
            return user_info
        except tweepy.TweepError as error:
            message = f'Error attempting to get user info. Error = {error}'
            print(message)
            return error


    def authenticate_to_account(self):
        print("Authenticating to Twitter API...")

        access_keys = self.access_keys

        # Authenticate to Twitter
        try:
            #consumer_key, consumer_secret
            auth = tweepy.OAuthHandler(access_keys['TWEEPY_CONSUMER_KEY'],access_keys['TWEEPY_CONSUMER_SECRET'])
                                    
            #access_token, acces_token_secret
            auth.set_access_token(access_keys['TWEEPY_ACCESS_TOKEN'], access_keys['TWEEPY_ACCESS_TOKEN_SECRET'])

            return tweepy.API(auth)
        except Exception as error:
            message = f'Error attempting to authenticate to account. Error = {error}'
            print(message)
            return error