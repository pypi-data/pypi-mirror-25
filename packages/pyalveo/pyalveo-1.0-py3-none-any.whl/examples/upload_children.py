import sys,os,random
import pyalveo
import time
from glob import glob
import csv

# disable insecure HTTPS warnings from the staging servers
import requests
requests.packages.urllib3.disable_warnings()

COLLECTION_NAME = "sc-cw-children"
#CONFIG = "examples/alveo-pc.config"
CONFIG = "/Users/steve/alveo.config"

EXT_MAP = {
    '.wav': "Audio",
    '.txt': "Text",
    '.sf0': "Pitch Track",
    '.sfb': "Formant Track",
    '.lab': "Annotation",
    '.trg': "Annotation",
    '.hlb': "Annotation",
}


DEMOGRAPHIC_MAP = {
    'Speakerid': 'dcterms:identifier',
    'Gender': 'foaf:gender',
    'ParentsLanguage': 'austalk:parents_first_langage',
    'OtherLanguage': 'austalk:other_languages',
    'Age': 'foaf:age',
    'POB': 'austalk:pob_town',
    'State': 'austalk:pob_state',
    'Country': 'austalk:pob_country',
    'Sibling': 'sibling'
    }

SPKR_DICT = None


def read_demographic(basedir):
    """Read the demographic spreadsheet and return a dict of dicts"""

    global SPKR_DICT

    if SPKR_DICT == None:

        SPKR_DICT = dict()
        with open(os.path.join(basedir, "sp1-sp8-demographic.csv")) as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                SPKR_DICT[row['Speakerid']] = row


def speaker_meta(speaker):
    """Return a dictionary of metadata for this speaker"""

    if speaker in SPKR_DICT:
        result = dict()
        for key in SPKR_DICT[speaker].keys():
            metakey = DEMOGRAPHIC_MAP[key]
            if SPKR_DICT[speaker][key] != '':
                result[metakey] = SPKR_DICT[speaker][key]
        return result
    else:
        return dict()


def create_speakers(basedir, client):
    """Create the speakers for the corpus

    """
    global SPKR_DICT

    read_demographic(basedir)
    for speaker in SPKR_DICT:
        meta = speaker_meta(speaker)
        speaker_uri = client.add_speaker(COLLECTION_NAME, meta)
        SPKR_DICT[speaker]['id'] = speaker_uri


def process(basedir):
    """Process the files in this corpus"""

    client = pyalveo.Client(configfile=CONFIG, verifySSL=False)

    create_speakers(basedir, client)

    collection_uri = client.api_url + "catalog/" + COLLECTION_NAME

    # delete any existing items
    print("Deleting items: ", list(client.get_items(collection_uri)))
    for itemuri in client.get_items(collection_uri):
        client.delete_item(itemuri)

    count = 0
    for itemid, meta, files in corpus_items(basedir):
        start = time.time()
        item = client.add_item(collection_uri, itemid, meta)
        print("Item: ", itemid, time.time()-start)

        for fn in files:
            docname = os.path.basename(fn)
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
                if docname.endswith('wav'):
                    client.add_document(item, docname, docmeta, displaydoc=True, file=fn)
                else:
                    client.add_document(item, docname, docmeta, file=fn)
                print("\tDocument: ", docname, time.time()-start)
            except pyalveo.pyalveo.APIError as e:
                print("Error: ", e)
                exit()

        count += 1
        if count > 1:
            return


def corpus_items(basedir):
    """Return an iterator over items in the corpus,
    each item is returned as a tuple: (itemid, metadata, [file1, file2, file3])
    where itemid is the identifier
    metadata is a dictionary of metadata
    fileN are the files to attach to the item
    """
    base_meta = {
        'dcterms:creator': 'C. Watson and S. Cassidy',
        "ausnc:mode": "spoken",
        "ausnc:communication_context": "face-to-face",
        "olac:language": "eng",
        "ausnc:interactivity": "read",
        "ausnc:audience": "individual",
        }

    read_demographic(basedir)

    for spkr in os.listdir(basedir):

        if not os.path.isdir(os.path.join(basedir, spkr)):
            continue
        meta = base_meta.copy()

        # grab the speaker identifier
        meta['olac:speaker'] = SPKR_DICT[spkr]['id']

        # iterate over wav files
        for wav in os.listdir(os.path.join(basedir, spkr, 'data')):
            files = []
            (sp, prompt, ext) = wav.split('.')

            if ext == 'wav':
                meta['dcterms:title'] = prompt
                meta['austalk:prompt'] = prompt

                # gather the files
                files.extend(glob(os.path.join(basedir, spkr, 'data', sp+'.'+prompt+'.*')))
                files.extend(glob(os.path.join(basedir, spkr, 'labels', sp+'.'+prompt+'.*')))

                yield (spkr + "." + prompt, meta, files)



if __name__=='__main__':

    basedir = sys.argv[1]

    process(basedir)
