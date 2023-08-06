from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from s3_uploader.exceptions.validation_exception import ValidationException
from s3_uploader.uploader.upload import upload_resource_and_return_version
from s3_uploader.uploader.validation import validate_file
from s3_uploader.utils.exception_handler import handle_exception
from s3_uploader.utils.utils import generate_json_output, print_output_message


def handle_resource_upload(args):
    """Main function to upload the resource to S3.

    The resource will be uploaded to the research binaries S3 repository,
    and a JSON output will be returned to the user to add to the microservice
    dependencies.json configuration file.

    :param args: The user's arguments supplied from the main function.
    """
    try:
        validate_file(args.file)
        version, s3_path = upload_resource_and_return_version(
            file_to_upload=args.file,
            bucket=args.bucket,
            bucket_path=args.s3_path)

        json_response = generate_json_output(
            args.file, args.location, version, s3_path)

        print_output_message(json_response)
        sys.exit()

    except ValidationException as ex:
        handle_exception(ex.message)

    except Exception:
        handle_exception('Unknown error occurred')
