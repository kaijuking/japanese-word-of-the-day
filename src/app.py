from getconfigvalues import get_twitter_account_info, get_database_name
from word import get_word_of_the_day
from tweet import Tweet


def lambda_handler(event, context):
    try:
        # Get a new random word from the database
        message = get_word_of_the_day()

        # Get the keys needed for the Twitter API
        access_keys = get_twitter_account_info()

        # Create a new Tweet instance
        new_tweet = Tweet(access_keys)

        # Post new message to Twitter account
        new_tweet.create_new_post(message)
    except Exception as error:
        message = f'Error occurred during invocation of lambda function. Error = {error}'
        print(message)
