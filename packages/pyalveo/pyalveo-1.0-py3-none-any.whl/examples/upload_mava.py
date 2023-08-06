# script to upload the MAVA corpus to Alveo

import sys,os,random
import pyalveo
import time
from glob import glob
import csv

from pprint import pprint

# disable insecure HTTPS warnings from the staging servers
import requests
requests.packages.urllib3.disable_warnings()

COLLECTION_NAME = "mava"
CONFIG = "examples/alveo.config"

EXT_MAP = {
    '.wav': "Audio",
    '.txt': "Tabular Data",  # lipcontours
    '.mp4': "Video",
    '.TextGrid': "Annotation",
}

META_MAP = {
    'AV_sync_s': 'mava:AV_sync_s',
    'AV_sync_spl': 'mava:av_sync_spl',
    'item_IEEE': 'mava:item_IEEE',
    'list_IEEE': 'mava:list_IEEE',
    'ref_x': 'mava:ref_x',
    'ref_y': 'mava:ref_y',
    'sent': 'dc:identifier',
    'sentence': 'austalk:prompt',
}

def read_item_meta(basedir):
    """Read the item metadata and return a dict of dicts indexed by the sentence id"""

    result = dict()

    with open(os.path.join(basedir, "MAVA.txt")) as fd:
        reader = csv.DictReader(fd, dialect='excel-tab')
        for row in reader:
            result[row['sent']] = dict()
            for key in row.keys():
                result[row['sent']][META_MAP[key]] = row[key]

    return result


def process(basedir):
    """Process the files in this corpus"""

    client = pyalveo.Client()
    client.add_context('mava', 'http://alveo.edu.au/mava')
    collection_uri = client.api_url + "catalog/" + COLLECTION_NAME

    # delete any existing items
    print "Deleting items: ", list(client.get_items(collection_uri))
    for itemuri in client.get_items(collection_uri):
        client.delete_item(itemuri)


    count = 0
    for itemid, meta, files in corpus_items(basedir):
        start = time.time()
        try:
            item = client.add_item(collection_uri, itemid, meta)
            print "Item: ", itemid, time.time()-start
        except pyalveo.pyalveo.APIError as e:
            print "Error: ", e
            continue

        for fname in files:
            docname = os.path.basename(fname)
            root, ext = os.path.splitext(docname)
            if ext in EXT_MAP:
                doctype = EXT_MAP[ext]
            else:
                doctype = "Other"

            docmeta = {
                       "dcterms:title": docname,
                       "dcterms:type": doctype
                      }
            try:
                client.add_document(item, docname, docmeta, file=fname)
                print "\tDocument: ", docname, time.time()-start
            except pyalveo.pyalveo.APIError as e:
                print "Error: ", e

        # count += 1
        # if count > 10:
        #     return



def corpus_items(basedir):
    """Return an iterator over items in the corpus,
    each item is returned as a tuple: (itemid, metadata, [file1, file2, file3])
    where itemid is the identifier
    metadata is a dictionary of metadata
    fileN are the files to attach to the item
    """

    itemmeta = read_item_meta(basedir)

    base_meta = {
            'dcterms:creator': 'Vincent Aubanel <v.aubanel@westernsydney.edu.au>',
            "ausnc:mode": "spoken",
            "ausnc:communication_context": "face-to-face",
            "olac:language": "eng",
            "ausnc:interactivity": "read",
            "ausnc:audience": "individual",
            'foaf:age': 21,
            'austalk:pob_town': "Camperdown",
            'austalk:pob_state': "NSW",
            'austalk:pob_country': "Australia",
            'austalk:first_language': "English",
            'austalk:mothers_first_language': 'English',
            'austalk:fathers_first_language': 'Italian'
    }

    for sent in os.listdir(os.path.join(basedir, 'sentences')):
        if sent in itemmeta:
            meta = base_meta.copy()
            meta.update(itemmeta[sent])

            files = os.listdir(os.path.join(basedir, 'sentences', sent))
            files = [os.path.join(basedir, 'sentences', sent, f) for f in files]

            yield (sent, meta, files)



if __name__=='__main__':

    basedir = sys.argv[1]
    from pprint import pprint

    process(basedir)
