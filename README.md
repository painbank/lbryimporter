Install internetarchive.py dependencies per:
  https://internetarchive.readthedocs.io/en/latest/installation.html

The 'ia' command line tool needs executed first to enable you to access the files and data remotely.
This will store your Internet Archive user info in the ~/.config/ia.ini file (on OSX).


Internet Archive

    To import content from Internet Archive, you must first identify the content by collection grouping
    as defined at the Internet Archive webstie.  For instance this address: https://archive.org/details/SciFi_Horror
    represents the SciFi_Horror collection of movies.  Narrowing down the size of the collection is suggested as
    the content is downloaded and then published.

Example of use:

    python lbryimporter -s internetarchive -a fav-cateliper

Notes on use:

1. This product is still in Beta and while functional, it is bare bones at the moment.
2. This tool checks for a prior import of files leveraging this tool and will not upload duplicates, although if the
    script version changes or downloaded content format changes, this may change or break.
2. No indicator of progress during download or upload is displayed.
3. Significant space may be used as the size of files is not checked.
4. The current version of the program is sequential, so only one file is downlaod and then upload before the next file
    is triggered.
5. It is possible to setup the script to only download, but it is currently not setup this way.
        IF a file has previously been downloaded by this script, it will not download the file a second time and will
        skip the download, provided the file is in the same location as previously downloaded.