import boto3


def get_twitter_account_info():

    params = [
        'TWEEPY_ACCESS_TOKEN', 
        'TWEEPY_ACCESS_TOKEN_SECRET', 
        'TWEEPY_CONSUMER_KEY', 
        'TWEEPY_CONSUMER_SECRET'
    ]

    keys = {
            'TWEEPY_CONSUMER_KEY': None, 
            'TWEEPY_CONSUMER_SECRET': None, 
            'TWEEPY_ACCESS_TOKEN': None, 
            'TWEEPY_ACCESS_TOKEN_SECRET': None
    }

    ssm = boto3.client('ssm')

    try:
        # Get the keys from SSM
        response = ssm.get_parameters(Names=params, WithDecryption=True)
        
        # Parse the response to get the actual values
        for item in response['Parameters']:
            name = item['Name']
            if name in keys:
                keys[name] = item['Value']

        return keys
    except Exception as error:
        message = f'Error retrieving information from SSM: {error}'
        print(message)


def get_database_name():
    params = [ 'TWEEPY_DB_TABLE' ]

    ssm = boto3.client('ssm')

    try:
        # Get the keys from SSM
        response = ssm.get_parameters(Names=params, WithDecryption=True)

        # Parse the response to get the actual values
        for item in response['Parameters']:
            if item['Name'] == 'TWEEPY_DB_TABLE':
                table_name = item['Value']

        return table_name
    except Exception as error:
        message = f'Error retrieving information from SSM: {error}'
        print(message)
