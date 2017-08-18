import os
from sys import argv
import requests
import wget
import json
from lxml import html, etree
from lxml.html.clean import clean_html
def print_links(folder, page_link):
    # folder = argv[1]
    # page_link = "".join(argv[2:])
    if not os.path.exists(folder):
        os.mkdir(folder)
    page = requests.get(page_link)
    tree = html.fromstring(clean_html(page.text))
    _mplinks = tree.xpath("//table//a/@href")
    mplinks = []
    for _mplink in _mplinks:
        if (_mplink[-3:]=="mp3"):
            mplinks.append(_mplink)
    mlink_list = []
    for mplink in mplinks:
	page = requests.get(mplink)
        tree2 = html.fromstring(clean_html(page.text))
        mlink = tree2.xpath("//b/a/@href")[-1]
        mlink_list.append({"a": mlink, "done": 0})
    with open('%s/list.json' % folder, 'w') as fp:
        json.dump(mlink_list, fp, indent=2)
    print "Wrote list.json :\n" , json.dumps(mlink_list, indent=2)

def download_links(folder):
    # folder = argv[1]
    with open('%s/list.json'% folder) as fp:
        mlink_list = json.load(fp)
    for i in range(len(mlink_list)):
        mlink = mlink_list[i]
	print "\n", i, json.dumps(mlink)
        if mlink['done'] == 0:
            wget.download(mlink['a'], folder)
            mlink_list[i]['done'] = 1
	    with open('%s/list.json'% folder, 'w') as fp:
		json.dump(mlink_list, fp, indent=2)
if __name__ == "__main__":
    print_links(argv[1], "".join(argv[2:]))
    download_links(argv[1])

