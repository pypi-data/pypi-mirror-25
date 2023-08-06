from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from datetime import datetime

from s3_uploader.utils import s3_utils
from s3_uploader.utils.utils import get_real_file_path


def upload_resource_and_return_version(file_to_upload, bucket,
                                       bucket_path=None):
    """This function responsible for uploading and versioning the resource.

    :param file_to_upload: A path to file to be uploaded.
    :param bucket: The name of the bucket.
    :param bucket_path: path to file in S3(without bucket name)
    :return: The version for the recent uploaded file.
    """
    file_name = os.path.basename(file_to_upload)
    version = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

    if not bucket_path:
        bucket_path = '/'.join([file_name, version, file_name])

    file_path = get_real_file_path(file_to_upload)
    s3_utils.upload(file_path, bucket, bucket_path)

    return version, bucket_path


