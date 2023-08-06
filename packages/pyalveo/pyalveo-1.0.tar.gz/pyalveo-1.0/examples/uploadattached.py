import sys,os,random
import pyalveo
import time

# disable insecure HTTPS warnings from the staging servers
import requests
requests.packages.urllib3.disable_warnings()


path = os.path.dirname(os.path.realpath(__file__))
client = pyalveo.Client(configfile="examples/alveo-pc.config" ,verifySSL=False,cache_dir="wrassp_cache")

collection_uri = client.api_url + "catalog/sctestcollection1"

# delete any existing items
print "Deleting items: ", list(client.get_items(collection_uri))
for itemuri in client.get_items(collection_uri):
    client.delete_item(itemuri)

text = """
Mrs Campbell was very much frightened and ill for three weeks afterwords but fortunately for me I had not the sense to be frightened. Indeed Mrs Campbell was so much frightened that she told me she had miscarried her twintyeth child but gude forgie  me I think she hardly sticks to the truth in family concerns she makes them all very young and for Mrs McLeod who has three children and is just about to have the fourth she is only twenty one or two and the young ladies three straping queens are from eighteen to fifteen but the youngest may pass for eighteen and the oldest for twinty six. Well we lost sight of St Jago and then we were becalmed for weeks together and but for harpooning sharks and shooting whales I dont know what the gentlemen would have done with themselves and the ladies generally were disputing which of their lords or brothers or lords to be (for there were some matches made up on the way) that had the merit of sending the poor shooten fishes to their long homes - And then, but this is rather a serious story, a young man of the name of Nicholson, a servant of Mrs Campbell, went to sleep in the jolly boat and was struck by the sun.  He died on the ninth day afterwards and was buried on the day after his death. I never never will forget the sound of the deep and hollow plunge when the body was consined  to its fathomless bed of rest. It was a calm day and every wave was as still as death till the mornin after his funeral when all at once there was a breeze got up and in twelve hours we were a hundred miles from poor Nicholson.
"""
starttime = time.time()


for j in range(4):
    #because we can't delete some items causing the script to crash
    #we upload with a randomish file name to prevent clashes
    i = int(random.random()*1000)
    itemname = "item-%d" % i
    docname = itemname + ".txt"

    itemstart = time.time()

    #we create the file we want to attach
    with open(os.path.join(path,docname),'w') as file:
        file.write(text)


    meta = {
            'dcterms:title': 'Test Item %d' % i,
            'dcterms:creator': 'A. Programmer',
            "ausnc:mode": "written",
            "ausnc:communication_context": "newspaper",
            "olac:language": "eng",
            "ausnc:discourse_type": "narrative",
            "ausnc:audience": "mass_market",
            "ausnc:customproperty": "value",
            }
    #add the item
    item = client.add_item(collection_uri, itemname, meta)

    print("Created item " + item)

    docstart = time.time()

    # add a document to the item
    docmeta = {
               "dcterms:title": "Sample Document",
               "dcterms:type": "Text"
              }
    #here 'file' is the string directory to the file to be uploaded, we're linking to the one we created above
    #client.add_document(item, docname, docmeta, file=os.path.join(path,docname), displaydoc=True)
    client.add_document(item, docname, docmeta, content=text, displaydoc=True)
    # remove the temporary file
    os.unlink(os.path.join(path,docname))

    print("\tAdded document " + docname)
    done = time.time()


print "Finished Script Successfully"
