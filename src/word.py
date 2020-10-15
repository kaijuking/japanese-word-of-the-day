import boto3
import random
from getconfigvalues import get_database_name


def get_word_of_the_day():

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

        random_item = random.choice(response['Items'])
        word = random_item['word']['S']
        pronunciation = random_item['pronunciation']['S']
        meaning = random_item['meaning']['S']

        if pronunciation == "":
            new_word = f'{word} = {meaning}'
        else:
            new_word = f'{word} ({pronunciation}) = {meaning}'
        return new_word
    except Exception as error:
        message = f'Error retrieving word from databse. Error = {error}'
        print(message)