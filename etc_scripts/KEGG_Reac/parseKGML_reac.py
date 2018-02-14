# Dongjo Ban
# Jordan Lab 2017
# Create KEGG DB for CoMet
# Python 2.x

import requests
import json
import re
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET
import sys # DEBUGGING

k = KEGG()
data = dict()
list_path = open("hsa_list.txt").read().replace('path:','').split('\n') # create list of hsa pathways
list_path.pop() # random blank entry removed

i = 0
for hsa in list_path:
	i+=1
	print("# of pathways processed: ",i)

	req_url = 'http://rest.kegg.jp/get/'+hsa+'/kgml'
	kmgl = requests.get(req_url)
	root = ET.fromstring(kmgl.text)
	
	for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root


		r_ids = [x.strip() for x in reaction.attrib["name"].split('rn:')[1:]]

		for r in r_ids:
			data[r] = reaction.attrib["type"]
			print r,data[r]

with open('KEGG_Reac.json','w') as f:
	json.dump(data, f)