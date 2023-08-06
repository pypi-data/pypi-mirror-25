import pyalveo
import re



if __name__ == '__main__':

    import sys, os

    dirname = sys.argv[1]

    client = pyalveo.Client()

    for dirpath, dirnames, filenames in os.walk(dirname):

        for fn in filenames:

            itemname, ext = os.path.splitext(fn)

            m = re.match('(\d_\d+_\d+_\d+_\d+)', itemname)
            if m:
                itemname = m.group(1)

                itemurl = 'https://app.alveo.edu.au/catalog/austalk/' + itemname

                try:
                    item = client.get_item(itemurl)

                    with open(os.path.join(dirpath,fn), 'r') as fd:
                        content = fd.read()

                    meta = {
                        "dcterms:title": "Transcription",
                        "dcterms:type": "Transcriber",
                    }

                    try:
                        result = client.add_document(itemurl, itemname+ext, meta, content)
                        print "OK", itemurl
                    except pyalveo.APIError as e:
                        print "Error uploading annotation", itemurl
                except pyalveo.APIError as e:
                    print "Error getting item", itemurl

            else:
                print "no match", itemname
