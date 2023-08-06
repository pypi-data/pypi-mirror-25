==========
FlickrSync
==========

A command line tool to synchronise pictures between the local file system and Flickr

    | https://github.com/danchal/flickrsync
    | https://pypi.python.org/pypi/flickrsync


Requirements
============

::

    Python3
    Pip
    ImageMagick
    A Flickr account

Install
=======

::

    $ sudo apt install python3-pip
    $ sudo apt install libmagickwand-dev
    $ sudo pip3 install flickrsync

References
==========

    | https://pypi.python.org/pypi/flickrapi
    | https://pypi.python.org/pypi/Wand
    | https://pypi.python.org/pypi/configparser
    | http://www.imagemagick.org
    | https://www.flickr.com/

Setup
=====

#. Create the configuration file

    - name the file $HOME/.flickrsync/config.ini
    - add your Flickr username, API Key and API Secret
    - edit your pictures directory as required
    - a template configuration file can be found somewhere in your python library ../flickrsync/etc/config.ini


#. Authenticate the FlickrSync application with Flickr (see usage, below)

Usage
=====

::

    To see a full list of commands
    $ flickrsync --help

    To authenticate FlickrSync with Flickr
    $ flickrsync auth

    To perform a one way sync from the local file system to Flickr
    $ flickrsync sync

    To perform a two way sync between the local file system and Flickr
    $ flickrsync sync2

    To create Flickr photosets based upon the local file system
    $ flickrsync photosets

Features
========

#. Duplicate copies of the same picture on the local file system are identified.

    - Image hash signature of the picture is used
    - only a single copy of the picture will be uploaded

#. Does not rely on the local pathname for identifying the picture.

    - moving a picture to a different directory will not cause the picture to be uploaded again

#. A SQLite database is used to index local and Flickr pictures.

    - destroying the database will not result in any pictures being uploaded again
    - database is automatically recreated

#.  Perform a two way sync between the local file system and Flickr.

#.  Multi-threaded.

Sync Process
============

::

    Local <==> Flickr

#. Creates an index of pictures on the local file system.
#. Creates an index of pictures on Flickr.
#. Download and scan unmatchable Flickr pictures.
#. Identify duplicate pictures on local file system.
#. Match local pictures to Flickr.
#. Upload unmatched local pictures to Flickr.
#. Download pictures from Flickr that are missing on the local file system.
#. Create Flickr photosets based upon the original filepath of the picture.

Picture Matching
================

    +----------------+------------------+----------------+---------+-----+---------+-----+
    |Local                              |Flickr                                          |
    +----------------+--------+---------+----------------+---------+-----+---------+-----+
    |DateTimeOriginal|Filename|Signature|DateTakenUnknown|DateTaken|Title|Signature|Match|
    +================+========+=========+================+=========+=====+=========+=====+
    |x               |x       |         |0               |x        |x    |         |yes  |
    +----------------+--------+---------+----------------+---------+-----+---------+-----+
    |                |        |x        |                |         |     |x        |yes  |
    +----------------+--------+---------+----------------+---------+-----+---------+-----+

    *Note: x indicates a match betwen local and Flickr*

#. Pictures will be matched by either:-

    - picture file name + date picture was taken, or
    - ImageMagick hash signature of picture

#. Date matching is turned on by default and can be disabled using the option [--nodatematch]. Use this option if you have pictures which do not have correct DateTimeOriginal.
#. Each uploaded picture is tagged with its ImageMagick hash signature.
#. Pictures on Flickr have a datetaken, https://www.flickr.com/services/api/misc.dates.html.
#. If the Flickr datetaken is generated from the pictures Exif data, then Flickr will set the DateTakenUnknown to 0.
#. If it exists, the Exif DateTimeOriginal is extracted from each picture on the local file system.
#. The Flickr title is based upon the original filename of the uploaded picture.
#. File names are compared without the file extension. This is because Flickr does not always maintain the file extension during upload as it is dependent upon the upload client used.

Photosets
=========

#. A photoset is based upon a flattened directory path of each picture.

#. Photosets created by FlickrSync are identified as such by their photoset description.

    - (re)creating the photosets could delete any photosets that are not being used
    - only photosets previously created by FlickrSync are deleted

Notes
=====

#. FlickrSync does NOT require sudo to run.
#. Pictures will not be deleted on either the local file system or Flickr.
