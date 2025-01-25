import boto3
import os
import pandas as pd
from helpers.logging_helper import LoggerHelper
from helpers.decorator_helper import frame, timeit_log


lg = LoggerHelper().create_logger('bedrock', 'info')


@timeit_log(lg)
def create_client(service: str) -> boto3.client:
    """Create a Boto3 client to authenticate an AWS session

    Args:
        service (str): The name of the service to create a client for

    Returns:
        boto3.client: The client created for the service
    """
    client = boto3.client(
        service_name=service,
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['AWS_DEFAULT_REGION'])
    lg.info(f"Bedrock client created: {client.__dict__}")
    return client

@timeit_log(lg)
def get_foundational_models(client: boto3.client) -> pd.DataFrame:
    """Create a requesting using Boto3 SDK to get a list of foundational models
    this account has access to using with the Bedrock service.

    Args:
        client (boto3.client): The client object to authenticate the session, used
        to make the request to the service.

    Raises:
        boto3.exceptions.ClientError: If there is an error with the client object
        boto3.exceptions.HTTPClientError: If there is a 4xx error while making the request for the list

    Returns:
        pd.DataFrame: The response from the service normalized as a dataframe
    """
    try:
        response = client.list_foundation_models()
    except boto3.exceptions.ClientError as e:
        lg.error(f"Client error: {e}")
        raise e
    except boto3.exceptions.HTTPClientError as e:
        lg.error(f"HTTP client error: {e}")
        raise e
    else:
        return pd.json_normalize(response, record_path='modelSummaries')

@timeit_log(lg)
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the response object by converting some of the values from a list
    to a single value, and renaming the columns to improve indexing.

    Args:
        df (pd.DataFrame): The response from the service normalized as a dataframe (list of foundational models

    Returns:
        pd.DataFrame: The response from the service normalized as a dataframe (list of foundational models) with some columns renamed and cleaned up. 
    """
    lg.info('Cleaning the dataframe')
    exploded_df = df.explode('outputModalities')\
                    .explode('responseStreamingSupported')\
                    .explode('inferenceTypesSupported')\
                    .explode('modelLifecycle.status')
    header = [
        'model_arn',
        'model_id',
        'model_name',
        'provider_name',
        'input_modalities',
        'output_modalities',
        'resp_streaming_supported',
        'customisations_supported',
        'inference_types_supported',
        'model_lifecycle_status'
        ]
    exploded_df.columns = header
    exploded_df.reset_index(drop=True, inplace=True)
    return exploded_df

@timeit_log(lg)
def query_datadrame(df: pd.DataFrame, query_str: str) -> pd.DataFrame:
    """Filter the respone object to return only active models that support text input and on-demand inference

    Args:
        df (pd.DataFrame): The response from the service with cleaned up columns

    Returns:
        pd.DataFrame: A subset of the cleaned up dataframe that meets the query criteria
    """
    lg.info('Filter the dataset to return only active models that support text input and on-demand inference')
    subset_df = df.query(query_str)
    subset_df.reset_index(drop=True, inplace=True)
    return subset_df

@frame
def main():
     bedrock = create_client('bedrock')
     resp_df = get_foundational_models(bedrock)
     cleaned_df = clean_dataframe(resp_df)
     query: str = "model_lifecycle_status == 'ACTIVE' and output_modalities == 'TEXT' and inference_types_supported == 'ON_DEMAND'"
     queried_df = query_datadrame(cleaned_df, query)
     filename: str = 'list_of_active_foundational_models.csv'
     queried_df.to_csv(filename, sep=',', index=False, header=True, encoding='utf-8')


if __name__ == "__main__":
     main()
