"""Get data from Austalk in Alveo,
finding speakers via metadata queries,
finding speaker metadata,
finding items for a speaker
downloading audio files from an item"""

from __future__ import print_function
import pyalveo
import os
from fnmatch import fnmatch


PREFIXES = """
PREFIX dc:<http://purl.org/dc/terms/>
PREFIX austalk:<http://ns.austalk.edu.au/>
PREFIX olac:<http://www.language-archives.org/OLAC/1.1/>
PREFIX ausnc:<http://ns.ausnc.org.au/schemas/ausnc_md_model/>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX dbpedia:<http://dbpedia.org/ontology/>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX iso639schema:<http://downlode.org/rdf/iso-639/schema#>
PREFIX austalkid:<http://id.austalk.edu.au/>
PREFIX iso639:<http://downlode.org/rdf/iso-639/languages#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX is: <http://purl.org/ontology/is/core#>
PREFIX iso: <http://purl.org/iso25964/skos-thes#>
PREFIX dada: <http://purl.org/dada/schema/0.2#>"""


def find_speakers(client):
    """Find speakers in Austalk and return
    a dictionary with one key per speaker
    and each key containing a dictionary of
    metadata values for that speaker"""

    query = PREFIXES + """
    select ?spkr ?id ?town ?country {
        ?spkr a foaf:Person .
        ?spkr austalk:id ?id .
        ?spkr austalk:pob_town ?town .
        ?spkr austalk:pob_country ?country .
    }
    limit 10
    """

    result = client.sparql_query('austalk', query)
    speakers = {}
    for b in result['results']['bindings']:
        speakers[b['spkr']['value']] = {'id': b['id']['value'],
                                        'town': b['town']['value'],
                                        'country': b['country']['value']
                                        }
    return speakers


def find_words(client, speakerid, words):
    """Find words in the Austalk corpus for a given speaker
    return an ItemGroup object containing the items
    """

    query = PREFIXES + """
SELECT distinct ?item ?prompt ?compname
WHERE {
  ?item a ausnc:AusNCObject .
  ?item olac:speaker <%s> .
  ?item austalk:prompt ?prompt .
  ?item austalk:componentName ?compname .
 """ % speakerid

    filterclause = 'FILTER regex(?prompt, "^'
    filterclause += '$|^'.join(words)
    filterclause += '$", "i")\n'

    query += filterclause + "}"

    result = client.sparql_query('austalk', query)

    items = []
    for b in result['results']['bindings']:
        itemurl = b['item']['value']
        # HACK: current database has the wrong URL for items - this will be fixed soon so this will be
        # redundant
        itemurl = itemurl.replace('http://id.austalk.edu.au/item/', 'https://app.alveo.edu.au/catalog/austalk/')
        items.append(itemurl)

    return pyalveo.ItemGroup(items, client)



def download_documents(item_list, patterns, output_path):
    """
    Downloads a list of documents to the directory specificed by output_path.

    :type documents: list of pyalveo.Document
    :param documents: Documents to download

    :type output_path: String
    :param output_path: directory to download to the documents to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    downloaded = []

    items = item_list.get_all()
    filtered_documents = []
    for item in items:
        documents = item.get_documents()
        for doc in documents:
            for pattern in patterns:
                if not pattern == '' and fnmatch(doc.get_filename(), pattern):
                    fname = doc.get_filename()
                    try:
                        doc.download_content(dir_path=output_path, filename=fname)
                        downloaded.append(fname)
                        print "Got ", fname
                    except:
                        # maybe it doesn't exist or we have no access
                        # TODO: report this
                        pass
    return downloaded


if __name__=='__main__':
    client = pyalveo.Client()
    speakers = find_speakers(client)

    hVdWords = {
        'monopthongs': ['head', 'had', 'hud', 'heed', 'hid', 'hood', 'hod', 'whod', 'herd', 'haired', 'hard', 'horde'],
        'dipthongs': ['howd', 'hoyd', 'hide', 'hode', 'hade', 'heared']
        }

    for speaker in speakers:
        print(speaker, speakers[speaker])
        items = find_words(client, speaker, hVdWords['dipthongs'])
        for item in items:
            print("\t", item)

        # download to a speaker specific directory
        outdir = os.path.join('out', speakers[speaker]['id'])
        download_documents(items, ["*speaker16.wav"], outdir)
