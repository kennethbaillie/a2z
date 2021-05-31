#!/opt/local/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import json
import unicodedata

sourcefile = "a2z.md"
outdir = "../cards"
si_file = "../searchindex.json"

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def get_unique_words(bigstring):
    deletelist = ['\ufb01','\u00e2','\u2021','\u2013','\ufb02','\ufb02','\ufb00','-','\u201c','\u201d']
    for char in deletelist:
        bigstring = bigstring.replace(char,'')
    for char in ['\t','.','[',']','(',')','{','}','"',"'"]:
        bigstring = bigstring.replace(char,' ')
    bs = [x.strip() for x in re.split(';| |,|\n|\r',bigstring)]
    bs = list(set([x for x in bs if len(x)>1]))
    return ' '.join(bs)
#---------------

with open(sourcefile) as f:
    text = f.read()

searchlist = []
blocks = text.split("\n# ")
for i,b in enumerate(blocks):
    lines = b.split("\n")
    lines[0] = lines[0].replace("#","")
    title = lines[0].strip()
    filename = slugify("".join(title.split(" ")[:3])).lower()[:50]
    lines[0] = "#" + lines[0]
    thisfile = os.path.join(outdir, filename+".md")
    with open(thisfile, "w") as o:
        o.write("# " + b)
    searchlist.append({
            'href': os.path.relpath(thisfile),
            'title': title,
            'content': get_unique_words(b), # this is the slow bit
            })

with open(si_file,"w") as o:
    json.dump(searchlist, o, indent=4)


















