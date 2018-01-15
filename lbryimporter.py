from internetarchive import download
from internetarchive import search_items
from internetarchive import get_item
import os
import csv
from os import listdir
from os.path import isfile, join
import requests
import sys
import getopt
import json

def previously_published(lbry_name=""):
    print("--------------------------\nChecking to see if the file " + lbry_name + " exists already in the blockchain.")
    url = "http://localhost:5279/lbryapi"

    params = {}
    params['uri'] = lbry_name
    data = {}
    data['params'] = params
    data['jsonrpc'] = '2.0'
    data['method'] = 'resolve'
    json_data = json.dumps(data)

    headers = {
        'cache-control': "no-cache"
        }
    response = requests.request("POST", url, data=json_data, headers=headers)
    response_text = response.json()
    result = response_text['result']
    name = result[lbry_name]

    if 'error' in name:
        # we don't need to match the name as the API does that for us.
        #print "The file %s doesn't exist on the blockchain." % lbry_name
        return False
    else:
        #print "The file %s exists on the blockchain" % lbry_name
        return True


def publish(channel_name, filename, fileAndPath, title="", description="", author="", language="en", license="", nsfw=False):
    url = "http://localhost:5279/lbryapi"

    lbryname = title.replace(" ", "-")
    lbryname = lbryname.replace("(", "")
    lbryname = lbryname.replace(")", "")
    lbryname = lbryname.replace("\"", "")
    lbryname = lbryname.replace("\'", "")

    if previously_published(lbryname):
        print "The file: " + filename + " -- already exists on the blockchain.\n Skipping the Publish."
    else:
        metadata = {}
        metadata['description'] = description
        metadata['title'] = title
        metadata['author'] = author
        metadata['thumbnail'] = ''
        metadata['language'] = language
        metadata['license'] = license       # TODO : What is the license for the IA content?
        metadata['nsfw'] = nsfw             # TODO : what does IA provide?  Is nsfw = false okay?
        params = {}
        params['metadata'] = metadata
        params['name'] = lbryname
        params['file_path'] = fileAndPath
        params['bid'] = 0.001
        params['channel_name'] = channel_name # TODO : verify what this function does w/o a name...

        data = {}
        data['params'] = params
        data['jsonrpc'] = '2.0'
        data['method'] = 'publish'
        json_data = json.dumps(data)

        headers = {
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url, data=json_data, headers=headers)
        if response.status_code == requests.codes.ok:
            print "Successfully published the file"
        else:
            print "something went wrong when trying to publish your file"
            print "APP Error - POST return code: " + response.status_code

def parseInternetArchive(collection=''):
    if collection != '':
        movies = search_items('collection:%s' % collection) #for example: fav-cateliper
    else:
        print("A collection name is required.\n")
        usage()
        sys.exit()

    for item in movies.iter_as_items():
        print("--------------------------\nDownloading: " + item.identifier)
        download(item.identifier, verbose=True, destdir="downloads", formats=['512Kb MPEG4', 'MPEG4'])
        # metadata
        meta = get_item(item.identifier)
        title = meta.item_metadata['metadata']['title']
        print "Title: " + title
        description = meta.item_metadata['metadata']['description']

        # ASSUMING you already have a channel, now add the file to the blockchain
        path = os.path.dirname(os.path.abspath(__file__)) + "/downloads/" + item.identifier + "/"

        # Process the downloaded files to find the movie to upload
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        parser = csv.reader(onlyfiles)

        mp4 = ".mp4"
        ogv = ".ogv"
        for fields in parser:
            for i, f in enumerate(fields):
                # TODO : update it to only publish a single image file, not all the movie files.
                if f.find(mp4) > 0:
                    publish('@internetarchive', f, path + f, title, description)
                elif f.find(ogv) > 0:
                    publish('@internetarchive', f, path + f, title, description)
                else:
                    notSupported() # TODO : How to handle other formats.  add display of file name/type that is being skipped.

def notSupported():
    #print "That format of a file isn't support yet for publishing, please visit the LBRY.io Discord chat for help"
    return


def usage():
    print "Thanks for importing your media into LBRY.  We appreciate the confidence.\n"
    print "     -h or --help : for this help menu\n"
    print "     -d : to turn on debug code\n"
    print "     -a or --archive-name : Internet Archive Collection Name\n"
    print "     -t or --type : the type of account to import: InternetArchive, Gutenburg or YouTube\n"
    print "\n An Internet Archive account login has to be setup first to be able to download movies."
    print "     follow these instructions for setting up your OS before running the internet archive importer to LBRY"
    print "     https://internetarchive.readthedocs.io/en/latest/installation.html"


def main(argv):
    print("main app started.")

    try:
        opts, args = getopt.getopt(argv, "hs:a:", ["help", "source=", "archive-name="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-a", "--archive-name"):
            archive = arg
        else:
            usage()
            sys.exit()

    if source == "internetarchive":
        parseInternetArchive(archive)
    elif source == "gutenberg" or source == "youtube":
        notSupported()
        sys.exit()
    else:
        print "Please specify the type of import you want to run.\nA type of archive is required.\n"
        usage()


if __name__ == "__main__":
    main(sys.argv[1:])
