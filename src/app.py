from tweet import Tweet
from word import get_words_from_database, transform_data_from_database, get_random_word
from getconfigvalues import get_twitter_account_info


def lambda_handler(event, context):
    try:
        # Get data from the database
        raw_data = get_words_from_database()

        # Transform the raw data
        data = transform_data_from_database(raw_data)
 
        # Get the keys needed for the Twitter API
        access_keys = get_twitter_account_info()

        # Create a new Tweet instance
        new_tweet = Tweet(access_keys)

        # Get last twenty timeline posts
        timeline_posts = new_tweet.get_last_twenty_posts()

        # Get a random word
        message = get_random_word(data, timeline_posts)
        print(f'message to post = {message}')

        # Post new message to Twitter account
        new_tweet.create_new_post(message)
    except Exception as error:
        message = f'Error occurred during invocation of lambda function. Error = {error}'
        print(message)
