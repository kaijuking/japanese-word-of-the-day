import boto3
import random
from getconfigvalues import get_database_name


def get_words_from_database():

    print('Attempting to get a new word...')
      
    # Setup the query params
    word_types = ['noun', 'verb', 'adjective', 'adverb']
    word_type = random.choice(word_types)
    exp_attributes = {':wt': {'S': word_type}}
    key_cond_exp = "wordtype = :wt"
    table_name = get_database_name()
    
    # Connect to DynamoDB
    dynamodb_client = boto3.client('dynamodb')
    try:
        response = dynamodb_client.query(
            
            ExpressionAttributeValues=exp_attributes, 
            
            KeyConditionExpression=key_cond_exp, 
            
            TableName=table_name,
            
            IndexName="wordtype-index"
        )

        return response['Items']

    except Exception as error:
        message = f'Error retrieving word from databse. Error = {error}'
        print(message)
        return 'Error retrieving word from databse.'


def transform_data_from_database(word_list):
    '''
        word_list: list returned from querying the database
    '''

    print('trying to transform data')

    transformed_word_list = []

    for item in word_list:
        
        word = item['word']['S']
        pronunciation = item['pronunciation']['S']
        meaning = item['meaning']['S']

        if pronunciation == "":
            new_word = f'Word: {word}, Meaning: {meaning} #Japanese #日本語'
        else:
            new_word = f'Word: {word}, Pronunciation: {pronunciation}, Meaning: {meaning} #Japanese #日本語'
        transformed_word_list.append(new_word)

    return transformed_word_list


def get_random_word(word_list, timeline_posts):
    '''
        word_list: transformed data from the database
        timeline_posts: a string list containing the last twenty posts from the user's timeline

    '''

    new_word = None

    try:

        for i in range(len(word_list)):
            if not word_list[i] in timeline_posts:
                new_word = word_list[i]
        
        if not new_word is None:
            return new_word
        else:
            default_post = [
                "Thank you for following MaikuOnline! #Japanese #日本語",
                "Want to learn more about Japanese language, daily life experiences, and cultural literacy? Than I highly recommend @JapanEverydayJP (https://japaneveryday.jp/)! #Japanese #日本語 #文化 #日常生活"
                ]
            return random.choice(default_post)

    except Exception as error:
        print(f'Error trying to get a random word. Error = {error}')
        return 'Error trying to get a random word.'