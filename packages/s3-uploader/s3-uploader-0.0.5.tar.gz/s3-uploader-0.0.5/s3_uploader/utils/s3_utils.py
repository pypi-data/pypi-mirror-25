from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import boto3
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError

from s3_uploader.utils.exception_handler import handle_exception

# Credentials are being read from shared credentials file configured for
# the AWS command line. Usually this configured as: ~/.aws/credentials

# More details at:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html#shared-credentials-file
s3_client = boto3.client('s3')


def upload(file_path, bucket, bucket_path):
    """This function wraps boto3's s3 upload function, accompanied with a 
    try/except mechanism for exception handling.
    
    At the moment, the exception handling is basic and practically doesn't 
    do much, but in the future can be extended.
    
    :param file_path: The path to the file to upload. 
    :param bucket: The name of the bucket.
    :param bucket_path: The key path inside the bucket for the file to be 
    stored at.
    :return: Nothing.
    """
    try:
        s3_client.upload_file(file_path, bucket, bucket_path)
    except (ClientError, ValueError, S3UploadFailedError) as ex:
        handle_exception(ex.message)
