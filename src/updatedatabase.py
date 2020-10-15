import boto3
import random
import uuid
import json
from urllib.parse import unquote_plus
from getconfigvalues import get_database_name


def update_database_with_new_data(event, context):
    
    print('Attempting to update the databse with new words...')

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
    except Exception as error:
        message = f'Error getting file from s3. Error = {error}'
        print(message)
        break

    # Get the table name
    table_name = get_database_name()

    # Update the database with new data
    dynamodb_client = boto3.client('dynamodb')
    for item in json_data:
        try:
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
        except Exception as error:
            message = f'Error updating database with new words. Error = {error}'
            print(message)
            break

    # Delete the file from s3
    s3_delete = boto3.client('s3')
    try:
        print("Deleting file from s3 bucket...")
        delete_response = s3_delete.delete_object(Bucket=bucket, Key=key)
        print(f'File Delete Response = {delete_response}')
    except Exception as error:
        message = f'Error deleting file from s3. Error = {error}'
        print(message)