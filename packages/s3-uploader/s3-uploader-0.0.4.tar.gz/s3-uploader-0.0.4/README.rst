===============================
S3 Uploader
===============================

.. image:: https://img.shields.io/pypi/d/s3-uploader.svg
    :target: https://pypi.python.org/pypi/s3-uploader/
    :alt: Downloads
.. image:: https://img.shields.io/pypi/v/s3-uploader.svg
    :target: https://pypi.python.org/pypi/s3-uploader/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/l/s3-uploader.svg
    :target: https://pypi.python.org/pypi/s3-uploader/
    :alt: License

Command line tool for uploading resources to AWS S3.

This is part of Onfido's team blobs store project.

The purpose of this tool is to upload and manage the versions of your project's
dependencies that later could be resolved by the complimentary tool
the `dependencies-resolver`.


Installing
==========

.. code-block:: shell

	$ pip install s3-uploader


How to use
==========
Example for using the tool to upload a resource

.. code-block:: shell

	s3-uploader -b my-s3-bucket -f my_big_blob -l path/to/blob/in/other/project

Or you can upload to a specific location in S3

.. code-block:: shell

	s3-uploader -b my-s3-bucket -f my_big_blob -p path/to/file/in/s3 -l path/to/blob/in/other/project


Get the project
===============

	1. Clone the git repository

	.. code-block:: shell

		$ git clone https://github.com/onfido/s3-uploader

	2. Install a virtualenv

	.. code-block:: shell

		$ sudo apt-get install python-virtualenv

	3. Create a new virtualenv

	.. code-block:: shell

		$ virtualenv s3_uploader_ve

	4. Install project's requirements

	.. code-block:: shell

		$ s3_uploader_ve/bin/pip install -r requirements.txt



Reporting Issues
================
If you have suggestions, bugs or other issues specific to this library, open
an issue, or just be awesome and make a pull request out of it.

