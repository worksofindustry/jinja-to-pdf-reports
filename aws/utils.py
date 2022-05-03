import boto3
from botocore.exceptions import ClientError
import pandas as pd
from sqlalchemy import create_engine
import base64
from json import loads


def get_secret() -> dict:
    secret_name = "<your-secret>"
    region_name = "<your-region>"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])
        return loads(secret)


def get_object_key(engine, file_id) -> str:
    query_str = f"select key from video_detail where id={file_id}"
    return pd.read_sql(query_str, engine)['key'][0]


def get_object_key(engine, file_id) -> str:
    query_str = f"select key from video_detail where id={file_id}"
    return pd.read_sql(query_str, engine)['key'][0]


def read_det_file(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_RESULTS_BUCKET, file_ID, engine):
    """removed from public repo"""
    pass
        