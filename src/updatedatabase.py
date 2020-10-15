import boto3
import uuid
import json
from urllib.parse import unquote_plus
from getconfigvalues import get_database_name


def update_database_with_new_data(event, context):
    
    try:
        # Parse the event from Cloudwatch
        records = event['Records']

        # Get the data from S3
        get_result = get_data_from_s3(records)

        # Parse the get_result to get the Bucket, Key and the Data
        key = get_result.get('key')
        bucket = get_result.get('bucket')
        json_data = get_result.get('data')

        # Update the databse with the JSON data
        update_result = update_database_with_new_words(json_data)
        
        # Delete the file from S3
        if update_result is True:
            delete_file_from_s3(bucket, key)
    except Exception as error:
        message = f'Error occurred during invocation of lambda function. Error = {error}'
        print(message)


def get_data_from_s3(records):
    s3_resource = boto3.resource('s3')
    print("Getting data from s3 bucket...")
    try:
        for record in records:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            obj = s3_resource.Object(bucket, key)
            data = obj.get()['Body'].read().decode('utf-8')
            json_data = json.loads(data)
            return {'bucket': bucket, 'key': key, 'data': json_data}
    except Exception as error:
        message = f'Error getting file from s3. Error = {error}'
        print(message)


def update_database_with_new_words(data):
    print('Attempting to update the databse with new words...')

    # Get the table name
    table_name = get_database_name()

    # Update the database with new data
    dynamodb_client = boto3.client('dynamodb')
    try:
        for item in data:
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
            dynamodb_client.put_item(TableName=table_name, Item=new_db_item)
    except Exception as error:
            message = f'Error updating database with new words. Error = {error}'
            print(message)
            
    return True


def delete_file_from_s3(bucket, key):
    s3_delete = boto3.client('s3')
    try:
        print("Attempting to delete the file from S3...")
        delete_response = s3_delete.delete_object(Bucket=bucket, Key=key)
        print(f'File deleted from S3. Response = {delete_response}')
    except Exception as error:
        message = f'Error deleting file from s3. Error = {error}'
        print(message)