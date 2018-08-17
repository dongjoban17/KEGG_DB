'''
Dongjo Ban
Python 2.7
Script for retrieving the list of genes specifically in KEGG's hsa pathways
'''

import requests
import json
import re
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET

k = KEGG()
data = dict()

# Create list of hsa pathways
list_path = open("hsa_list.txt").read().replace('path:','').split('\n')
# Remove newline
list_path.pop()

i = 0
for hsa in list_path:
	i+=1
	print "# of pathways processed: ",i
	req_url = 'http://rest.kegg.jp/get/'+hsa+'/kgml'
	kmgl = requests.get(req_url)
	root = ET.fromstring(kmgl.text)
	
	for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root
		id_look = reaction.attrib["id"]
		for entry in root.findall("./entry"):
			if entry.attrib["id"]==id_look:
				gene_ids = entry.attrib["name"].split(' ')
				for gene in gene_ids:
					data[gene]=0

with open('KEGG_Gene.json','w') as f:
	json.dump(data, f)
