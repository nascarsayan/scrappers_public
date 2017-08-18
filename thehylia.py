import os
from sys import argv
import requests
import wget
from lxml import html, etree
from lxml.html.clean import clean_html
folder = argv[1]
page_link = "".join(argv[2:])
if not os.path.exists(folder):
    os.mkdir(folder)
page = requests.get(page_link)
tree = html.fromstring(clean_html(page.text))
_mplinks = tree.xpath("//table//a/@href")
mplinks = []
for _mplink in _mplinks:
    if (_mplink[-3:]=="mp3"):
        mplinks.append(_mplink)
for mplink in mplinks:
    mpage = requests.get(mplink)
    tree2 = html.fromstring(clean_html(mpage.text))
    mlink = tree2.xpath("//b/a/@href")[-1]
    wget.download(mlink, folder)
