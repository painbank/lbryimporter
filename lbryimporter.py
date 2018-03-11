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
import untangle

_debug = False


def lbry_api_status():
    print("--------------------------\nChecking to see LBRY daemon is running.")
    url = "http://localhost:5279/lbryapi"

    data = {}
    data['jsonrpc'] = '2.0'
    data['method'] = 'status'
    json_data = json.dumps(data)

    headers = {
        'cache-control': "no-cache"
        }
    try:
        response = requests.request("POST", url, data=json_data, headers=headers)
    except requests.ConnectionError:
        print "=*=" * 35
        print "ERROR: The LBRY app or daemon must be running to import files into LBRY."
        print "=*=" * 35
        sys.exit()

    print response
    if response.status_code is 200:
        return True
    else:
        return False

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
    try:
        response = requests.request("POST", url, data=json_data, headers=headers)
    except requests.ConnectionError:
        print "=*=" * 35
        print "ERROR: The LBRY app or daemon must be running to import files into LBRY."
        print "=*=" * 35
        sys.exit()

    response_text = response.json()
    result = response_text['result']
    name = result[lbry_name]

    if 'error' in name:
        # we don't need to match the name as the API does that for us.
        if _debug:
            print "The file %s doesn't exist on the blockchain." % lbry_name
        return False
    else:
        if _debug:
            print "The file %s exists on the blockchain" % lbry_name
        return True


def publish(channel_name, filename, fileAndPath, title="", description="", author="", language="en", license="", nsfw=False):
    url = "http://localhost:5279/lbryapi"

    lbryname = title.replace(" ", "-")
    lbryname = lbryname.replace("(", "")
    lbryname = lbryname.replace(")", "")
    lbryname = lbryname.replace("\"", "")
    lbryname = lbryname.replace("\'", "")
    lbryname = lbryname.replace(",", "")

    if previously_published(lbryname):
        print "The file: " + filename + " -- already exists on the blockchain.\n Skipping the Publish."
    else:
        metadata = {}
        metadata['description'] = description
        metadata['title'] = title
        metadata['author'] = author
        metadata['thumbnail'] = ''
        metadata['language'] = language
        metadata['license'] = license
        metadata['nsfw'] = nsfw
        params = {}
        params['metadata'] = metadata
        params['name'] = lbryname
        params['file_path'] = fileAndPath
        params['bid'] = 0.001
        if channel_name != "":                # Anonymous posting requires no channel_name in API call.
            params['channel_name'] = channel_name

        data = {}
        data['params'] = params
        data['jsonrpc'] = '2.0'
        data['method'] = 'publish'
        json_data = json.dumps(data)

        headers = {
            'cache-control': "no-cache"
        }
        if _debug:
            print '=' * 70
            print "LBRY PUBLISH API metadata is:"
            print "Lbryname publish name is = " + lbryname
            print "Lbryname channel name is = " + channel_name
            print "Title is = " + title
            print "Description = " + description
            print "Author = " + author
            print "Language is = " + language
            print "License url is = " + license
            print "NSFW flat is = " + str(nsfw)
            print "Lbryname publish name is = " + lbryname
            print "JSON data is - " + json_data
            print '=' * 70

        response = requests.request("POST", url, data=json_data, headers=headers)
        if response.status_code == requests.codes.ok:
            print "Successfully published the file"
        else:
            print "=*=" * 35
            print "something went wrong when trying to publish your file"
            print "APP Error - POST return code: " + str(response.status_code)
            print "You may want to exit and review the LBRY logs or report the issue."
            print "=*=" * 35



def parse_internet_archive(collection='', channel=''):
    if collection != '':
        movies = search_items('collection:%s' % collection)
    else:
        print("A collection name is required for importing Internet Archive content.\n")
        print "  use -h for help with more command line arguments"
        sys.exit()

    for item in movies.iter_as_items():
        print("--------------------------\nDownloading: " + item.identifier)
        # note - currently this will download all movie formats that match mpeg4
        download(item.identifier, verbose=True, destdir="downloads", formats=['512Kb MPEG4', 'MPEG4'])
        # metadata
        meta = untangle.parse("downloads/" + item.identifier + "/" + item.identifier + "_meta.xml")

        try:
            title = meta.metadata.title.cdata
        except AttributeError:
            try:
                title = meta.metadata.title[0].cdata    #there are duplicate entries in the xml, take the 1st
            except AttributeError:
                print "Skipping import - Unable to find a title for : " + item.identifier
                return
        try:
            description = meta.metadata.description.cdata
        except AttributeError:
            try:
                description = meta.metadata.description[0].cdata    #there are duplicate entries in the xml, take the 1st
            except AttributeError:
                print "Skipping import - Unable to find a description for : " + item.identifier
                return
        try:
            author = meta.metadata.director.cdata
        except AttributeError:
            try:
                author = meta.metadata.publisher.cdata
            except AttributeError:
                author = ""

        try:
            language = meta.item_metadata.language.cdata
            if language == 'english':
                language = 'en'
        except AttributeError:
            language = 'en'

        try:
            license = meta.metadata.licenseurl.cdata
        except AttributeError:
            license = 'public'

        if _debug:
            print '=' * 70
            print "Metadata found is:"
            print "Title is = " + title
            print "Description = " + description
            print "Author = " + author
            print "Language is = " + language
            print "License url is = " + license
            print '=' * 70

        # now add the file to the blockchain
        path = os.path.dirname(os.path.abspath(__file__)) + "/downloads/" + item.identifier + "/"

        # Process the downloaded files to find the movie to upload
        try:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            parser = csv.reader(onlyfiles)
        except OSError:
            print "No file exists here that was downloaded"

        mp4 = ".mp4"
        ogv = ".ogv"
        for fields in parser:
            for i, f in enumerate(fields):
                if f.find(mp4) > 0:
                    publish(channel, f, path + f, title, description, author, language, license)
                elif f.find(ogv) > 0:
                    publish(channel, f, path + f, title, description, author, language, license)
                else:
                    file_not_supported(f)


def file_not_supported(file_name):
    if _debug:
        print "That format of the " + file_name + " file isn't supported by this importer."
    return


def source_not_supported(source):
    print "The " + source + " source of data isn't support yet for publishing, please visit the LBRY.io Discord chat for help"
    return


def usage(opts=''):
    print "\n Help Information:\n"
    print "     -h or --help : for this help menu\n"
    print "     -d : to turn on debug code\n"
    print "     -s or --source : the source of the account to import: InternetArchive, Gutenburg or YouTube\n"
    print "     -a or --archive-name : Internet Archive Collection Name\n"
    print "     -c or --channel-name : The LBRY channel name to be associated with the import. Anonymous will be used if not specified.\n"
    print "\n An Internet Archive account login has to be setup first to be able to download movies."
    print "     follow these instructions for setting up your OS before running the internet archive importer to LBRY"
    print "     https://internetarchive.readthedocs.io/en/latest/installation.html"
    print "\nThank you for importing your media into LBRY.  We appreciate the confidence.\n"

    if _debug:
        print "Your Command Line arguments are: "
        for opt, arg in opts:
            print opt + " is " + arg


def main(argv):
    print("main app started.")
    print("verifing LBRY daemon is running.")
    if lbry_api_status() is False:
        print("ERROR - Exiting")
        sys.exit()

    source = ""
    channel = ""
    archive = ""
    global _debug
    try:
        opts, args = getopt.getopt(argv, "hds:a:c:", ["help", "source=", "archive-name=", "channel-name"])
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
        elif opt in ("-c", "--channel-name"):
            channel = arg
        else:
            usage()
            sys.exit()

    if _debug:
        print "Your Command Line arguments are: "
        for opt, arg in opts:
            print opt + " is " + arg

    if source == "internetarchive":
        parse_internet_archive(archive, channel)
    elif source == "gutenberg" or source == "youtube":
        source_not_supported(source)
        sys.exit()
    else:
        print "Please specify the type of import you want to run.\nA type of archive is required.\n"
        print "  use -h for help with more command line arguments"


if __name__ == "__main__":
    main(sys.argv[1:])
