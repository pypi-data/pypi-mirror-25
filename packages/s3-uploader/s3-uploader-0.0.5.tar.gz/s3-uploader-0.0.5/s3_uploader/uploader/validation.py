from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from s3_uploader.exceptions.validation_exception import ValidationException
from s3_uploader.utils.utils import get_real_file_path


def validate_file(file_to_upload):
    """Validating the file path.

    Validation rules are:
    1. Path should contain a file at the end and not point to a directory.
    2. File should be accessible so it can be uploaded.

    In case the path is relative, we'll use the OS current working directory
    and join its path with the given file path.

    In case of any violation of the validation process,
    an exception will be raised.

    :param file_to_upload: The path to the file. Can be either relative or
    absolute path.
    
    :return: True if everything goes by the rules, a ValidationException 
    otherwise.
    """
    upload_file_path = get_real_file_path(file_to_upload)

    if os.path.isdir(upload_file_path):
        raise ValidationException('Path should contain file at the end')

    # Verifying that the file is accessible before uploading
    try:
        with open(upload_file_path, 'rb'):
            pass
    except IOError:
        raise ValidationException('The file could not be opened. Check path '
                                  'and/or permissions')
    return True
