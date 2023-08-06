from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from s3_uploader.utils.utils import get_real_file_path


def test_get_real_file_path_absolute():
    """A test to check the functionality of the get_real_file_path function.
    An absolute path is being passed to the function, and so we expect the 
    path to stay as is.
    
    :return: True, unless the function is not working as we expected.
    """
    absolute_path = '/tmp'
    path = get_real_file_path(absolute_path)
    assert path == absolute_path


def test_get_real_file_path_relative():
    """A test to check the functionality of the get_real_file_path function.
    A relative path is being passed to the function, and so we expect the 
    path to be returned as absolute path in respect to the current working 
    directory.
    
    :return: True, unless the function is not working as we expected.
    """
    relative_path = 'path/to/file'
    path = get_real_file_path(relative_path)
    expected_path = os.path.join(os.getcwd(), relative_path)
    assert path == expected_path
