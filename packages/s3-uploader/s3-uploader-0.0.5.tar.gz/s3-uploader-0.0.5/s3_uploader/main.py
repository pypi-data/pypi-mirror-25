from __future__ import division
from __future__ import print_function

import argparse

from uploader.handle_resource import handle_resource_upload


def create_parser():
    """A function to create the argument parser to parse the user's input.
    
    :return: The argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='file',
                        required=True, action='store',
                        help='The file path to be uploaded. Can either be '
                             'relative or absolute path')
    parser.add_argument('-l', '--location', dest='location',
                        required=True, action='store',
                        help='The location in which the file should be '
                             'placed in the microservice. This location '
                             'should be a relative path regarding the '
                             'microservice root folder. This is for '
                             'generating the JSON to add '
                             'to the dependencies configuration file')
    parser.add_argument('-b', '--bucket', dest='bucket',
                        required=True, action='store',
                        help='The name of the bucket to use.')
    parser.add_argument('-p', '--s3-path', dest='s3_path',
                        action='store',
                        help='Path to the file in S3')
    return parser


def parse_arguments():
    """A function to parse the user's arguments and return an object which 
    holds the user's parsed arguments.
    
    :return: The user's parsed arguments as object.
    """
    parser = create_parser()
    args = parser.parse_args()
    return args


def main():
    """The main function to handle the user's input."""
    arguments = parse_arguments()
    handle_resource_upload(arguments)


if __name__ == '__main__':
    main()
