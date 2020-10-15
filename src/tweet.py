import tweepy


class Tweet:
    def __init__(self, access_keys):
        print('initializing new Tweet object')
        self.access_keys = access_keys
        self.api = self.authenticate_to_account()
        

    def get_default_post(self):
        default_post = 'Thank you for following MaikuOnline! 毎日頑張りましょう！'
        return default_post


    def create_new_post(self, message):
        print('Attempting to post a new message...')
        try:
            last_post = self.get_last_post()

            if not last_post == message:
                response = self.api.update_status(message)
            else:
                message = self.get_default_post()
                response = self.api.update_status(message)

            return response
        except Exception as error:
            message = f'Error attempting to post to account. Error = {error}'
            print(message)

    
    def get_last_post(self):
        try:
            last_tweet = self.api.home_timeline()
            return last_tweet[0].text
        except Exception as error:
            message = f'Error attempting to get last post. Error = {error}'
            print(message)

    
    def authenticate_to_account(self):
        print("Authenticated to Twitter API...")

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