# Overview

This importer python script is meant to allow easy importing of of content for the decentralized content marketplace provided by the [LBRY](https://lbry.io/) protocol.  Currently supported source of imported files is the Internet Archive.  Current files supported are .mp4 and .ogv formated MPEG4 videos.  

Future additions may include Gutenburg, YouTube or local files.  

## Dependencies:

* LBRY daemon must be running to enable this script to work properly.  The daemon can be downloaded and 
run from the [code](https://github.com/lbryio/lbrycrd) or by downloading and running the [LBRY app here](https://lbry.io)

* Python v2.7.10 minimum

* Install [internetarchive.py dependencies](https://internetarchive.readthedocs.io/en/latest/installation.html) per:

      https://internetarchive.readthedocs.io/en/latest/installation.html

* Usage of the Internet Archive (IA) API requires a local storage of the IA login. The 'ia' command line tool needs executed first to enable you to access the files and data remotely.
This will store your Internet Archive user info in the ~/.config/ia.ini file (on OSX).

  You can enable this through using IA Binaris show below.

* #### IA Binaries
Binaries are available for the ia command-line tool:

      $ curl -LOs https://archive.org/download/ia-pex/ia
      $ chmod +x ia
Binaries are generated with PEX. The only requirement for using the binaries is that you have Python installed on a Unix-like operating system.

    For more details on the IA command-line interface please refer to the [README](https://github.com/jjjake/internetarchive/blob/master/README.rst), or 'ia help'.

## Internet Archive:

* To import content from Internet Archive, you must first identify the content by collection grouping as defined at the Internet Archive website.  For instance this address:     

      https://archive.org/details/SciFi_Horror

* represents the __SciFi_Horror__ collection of movies.  Narrowing down the size of the collection is suggested as
    the content is downloaded and then published.


## Examples of use:

* The following examples infer that the above dependencies are properly setup first.  It also assumes the @intnernetarchive channel name is already reserved in LBRY or use one you already have reserved.

      python lbryimporter.py -s internetarchive -a SciFi_Horror -c @internetarchive
      python lbryimporter.py -source=internetarchive --archive-name=SciFi_Horror --channel-name=@internetarchive
      python lbryimporter.py -h


### Notes on use:

1. This tool checks for a prior import of files leveraging this tool and will not upload duplicates.
2. No indicator of progress during download or upload is displayed.
3. Significant space may be used as the size of files downloaded are not checked.
4. The current version of the program is sequential, so only one file is downloaded and then uploaded before the next file is triggered.
5. It is possible to setup the script to only download, but it is currently not setup this way.  IF a file has previously been downloaded by this script, it will not download the file a second time and will skip the download, provided the file and script location is in the same location as previously run.

## Additional Help info

Running the following command provides help information about command line arguments:

    $python lbryimporter.py -h

    main app started.

    Help Information:

         -h or --help : for this help menu

         -d : to turn on debug code

         -s or --source : the source of the account to import: InternetArchive, Gutenburg or YouTube

         -a or --archive-name : Internet Archive Collection Name

         -c or --channel-name : The LBRY channel name to be associated with the import. Anonymous will be used if not specified.


    An Internet Archive account login has to be setup first to be able to download movies.
         follow these instructions for setting up your OS before running the internet archive importer to LBRY
         https://internetarchive.readthedocs.io/en/latest/installation.html

    Thank you for importing your media into LBRY.  We appreciate the confidence.
