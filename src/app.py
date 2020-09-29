import tweepy
import boto3
import botocore
import random
import uuid
import csv
import json
from urllib.parse import unquote_plus

def lambda_handler(event, context):

    # Get needed varialbles from ssm
    app_keys = get_keys()

    # Authenticate to Twitter API    
    tweepy_api = authenticate_to_twitter(app_keys)

    # Get last post from twitter
    last_post = get_last_tweet(tweepy_api)

    # Get new word to post
    new_post = get_word_of_the_day(tweepy_api, app_keys)

    # Post a tweet
    post_tweet(tweepy_api, new_post, last_post)


def get_keys():
    names = [
        'TWEEPY_ACCESS_TOKEN', 
        'TWEEPY_ACCESS_TOKEN_SECRET', 
        'TWEEPY_CONSUMER_KEY', 
        'TWEEPY_CONSUMER_SECRET',
        'TWEEPY_DB_TABLE'
        ]
    ssm = boto3.client('ssm')

    try:
        tweepy_parameters = ssm.get_parameters(Names=names, WithDecryption=True)
    except botocore.exceptions.ParamValidationError as error:
        process_error(error, 'aws')

    return tweepy_parameters


def authenticate_to_twitter(key_list: list):
    print("Authenticating to Twitter...")
    
    keys = {
        'TWEEPY_CONSUMER_KEY': None, 
        'TWEEPY_CONSUMER_SECRET': None, 
        'TWEEPY_ACCESS_TOKEN': None, 
        'TWEEPY_ACCESS_TOKEN_SECRET': None
    }
    
    for item in key_list['Parameters']:
        name = item['Name']
        if name in keys:
            keys[name] = item['Value']
        
    # Authenticate to Twitter
    try:
        #consumer_key, consumer_secret
        auth = tweepy.OAuthHandler(keys['TWEEPY_CONSUMER_KEY'],keys['TWEEPY_CONSUMER_SECRET'])
                                
        #access_token, acces_token_secret
        auth.set_access_token(keys['TWEEPY_ACCESS_TOKEN'], keys['TWEEPY_ACCESS_TOKEN_SECRET'])

        print("Authenticated to Twitter API...")
        return tweepy.API(auth)
    except tweepy.TweepError as error:
        process_error(error, 'tweepy')


def get_last_tweet(api):

    # Get the last tweet from the timeline
    try:
        timeline = api.home_timeline()
        if len(timeline) > 0:
            return timeline[0].text
        else:
            return ""
    except tweepy.TweepError as error:
        process_error(error, 'tweepy')

    
def get_word_of_the_day(api, key_list: list):
      
    # Get the database table name
    for item in key_list['Parameters']:
        if item['Name'] == 'TWEEPY_DB_TABLE':
            table_name = item['Value']

    # Setup the query params
    word_types = ['noun', 'verb', 'adjective', 'adverb']
    word_type = random.choice(word_types)
    exp_attributes = {':wt': {'S': word_type}}
    key_cond_exp = "wordtype = :wt"
    
    # Connect to DynamoDB and send the query
    dynamodb_client = boto3.client('dynamodb')
    try:
        print('inside try block of get_word_of_the_day 1')
        response = dynamodb_client.query(
            
            ExpressionAttributeValues=exp_attributes, 
            
            KeyConditionExpression=key_cond_exp, 
            
            TableName=table_name,
            
            IndexName="wordtype-index"
        )
        print('inside try block of get_word_of_the_day 2')

        random_item = random.choice(response['Items'])

        new_word = random_item['word']['S']
        pronunciation = random_item['pronunciation']['S']
        meaning = random_item['meaning']['S']

        if pronunciation == "":
            new_post = f'{new_word} = {meaning}'
        else:
            new_post = f'{new_word} ({pronunciation}) = {meaning}'
        return new_post
    except botocore.exceptions.ClientError as error:
        process_error(error, 'aws')


def get_last_tweet(api):
    # Get the last posted tweets
    last_tweet = api.home_timeline()

    return last_tweet[0].text


def post_tweet(api, new_post: str, previous_post: str):

    tweet_msg = None
    if not new_post == previous_post:
        tweet_msg = new_post
    else:
        tweet_msg = get_default_post()

    # Update twitter timeline with new tweet
    try:
        print("Sending the tweet...")
        api.update_status(tweet_msg)
        print("Tweet successfully posted...")
    except tweepy.TweepError as error:
        process_error(error, 'tweepy')


def get_default_post():
    return "Thank you for following MaikuOnline! 毎日頑張りましょう！"


def process_error(error, error_source: str):
    if error_source == 'aws':
        error_code = error['Error']['Code']
        error_message = error['Error']['Message']
        http_status_code = error['ResponseMetadata']['HTTPStatusCode']
        print(f'Error Code = {error_code}.\n' +
              f'Error Message = {error_message}.\n' +
              f'HTTP Status Code = {http_status_code}')
    elif error_source == 'tweepy':
        print(f'Error Message = {error}')
    elif error_source == "lambda":
        print(f'Lambda function was invoked by an unknown source. Context = {error}')


def update_database_with_new_data(event, context):
    
    # Process the event from s3
    key = None
    bucket = None
    json_data = None
    records = event['Records']
    s3_resource = boto3.resource('s3')
    try:
        print("Getting data from s3 bucket...")
        for record in records:
            print("Parsing data returned from s3 bucket...")
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            obj = s3_resource.Object(bucket, key)
            data = obj.get()['Body'].read().decode('utf-8')
            json_data = json.loads(data)
    except botocore.exceptions.ClientError as error:
        process_error(error, 'aws')

    # Get the table name
    print("Getting the table name...")
    keys = get_keys()
    for item in keys['Parameters']:
        if item['Name'] == 'TWEEPY_DB_TABLE':
            table_name = item['Value']

    # Update the database with new data
    dynamodb_client = boto3.client('dynamodb')
    for item in json_data:
        try:
            print("Attempting to update the table with new items...")
            id = uuid.uuid4()
            word_type = item['wordtype']
            word_category = item['wordcategory']
            word = item['word']
            pronunciation = item['pronunciation']
            meaning = item['meaning']
            new_db_item = {
                'wordid': {'S': f'{id}'},
                'wordtype': {'S': f'{word_type}'},
                'wordcategory': {'S': f'{word_category}'},
                'word': {'S': f'{word}'},
                'pronunciation': {'S': f'{pronunciation}'},
                'meaning': {'S': f'{meaning}'}
            }
            response = dynamodb_client.put_item(TableName=table_name, Item=new_db_item)
        except botocore.exceptions.ClientError as error:
            process_error(error, 'aws')
            break

    # Delete the file from s3
    s3_delete = boto3.client('s3')
    try:
        print("Deleting file from s3 bucket...")
        delete_response = s3_delete.delete_object(Bucket=bucket, Key=key)
        print(f'File Delete Response = {delete_response}')
    except botocore.exceptions.ClientError as error:
        process_error(error, 'aws')
