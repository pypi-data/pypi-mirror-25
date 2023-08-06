"""Example script download the audio data corresponding to the
Dolby transcriptions.

To run this script you need to install the pyalveo library
which is available at (https://pypi.python.org/pypi/pyalveo/0.4) for
installation with the normal Python package tools (pip install pyalveo).

You also need to download your API key (alveo.config) from the Alveo web application
(click on your email address at the top right) and save it in your home directory:

Linux or Unix: /home/<user>
Mac: /Users/<user>
Windows: C:\\Users\\<user>

The script should then find this file and access Alveo on your behalf.

 """
from __future__ import print_function
import os
import pyalveo

# directory to write downloaded data into
outputdir = "data"

if __name__=='__main__':

    client = pyalveo.Client(use_cache=False)

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # look at the files in the out directory
    for trfile in os.listdir('out'):
        itemname = trfile.split('-')[0]
        # strip a trailing letter if present
        if itemname[-1] in ['A', 'B']:
            itemname = itemname[:-1]
        # get a wav file name
        wavname = os.path.splitext(trfile)[0]+".wav"

        itemurl = 'https://app.alveo.edu.au/catalog/austalk/'+itemname
        docurl = itemurl + "/document/" + wavname

        print("Downloading", docurl)
        try:
            doc = pyalveo.Document({'alveo:url': docurl}, client)
            doc.download_content(dir_path=outputdir)
        except:
            print("\tNot found")
