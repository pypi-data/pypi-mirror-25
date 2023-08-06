from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tempfile

import pytest

from s3_uploader.exceptions.validation_exception import ValidationException
from s3_uploader.uploader.validation import validate_file


def test_validate_file_is_dir():
    """A test to check the functionality of the validate_file function.
    A path to a directory is passed to the function, and so we expect to get a 
    ValidationException exception to be raised as this is not an accessible 
    file path.
     
    :return: Nothing. A ValidationException should be raised. 
    """
    with pytest.raises(ValidationException):
        path = '/tmp/'
        validate_file(path)


def test_validate_file_is_not_accessible():
    """A test to check the functionality of the validate_file function.
    A path to a non-accessible file is passed to the function, and so we 
    expect to get a ValidationException exception to be raised as this is not 
    an accessible file path.

    :return: Nothing. A ValidationException should be raised. 
    """
    with pytest.raises(ValidationException):
        path = '/root/some_file'
        validate_file(path)


def test_validate_file_good():
    """A test to check the functionality of the validate_file function.
    A path to an accessible file is passed to the function, and so we 
    expect the function to return True as the path to the file is accessible.

    :return: True, unless the function is not working as we expected. 
    """
    f = tempfile.NamedTemporaryFile()
    is_validate = validate_file(f.name)
    f.close()
    assert is_validate is True
