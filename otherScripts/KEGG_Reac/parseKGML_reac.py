'''
Dongjo Ban
Python 2.7
Script for examining KEGG reaction information
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
dup = {}
reac = {}
for hsa in list_path:
	i+=1
	print("# of pathways processed: ",i)
	kgml = open("../KEGG_DB_PATH/pathways/path_"+hsa).read()
	root = ET.fromstring(kgml)
	
	for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root
		r_ids = [x.strip() for x in reaction.attrib["name"].split('rn:')[1:]]
		for r in r_ids:
			if r in data.keys():
				if data[r][0] != reaction.attrib['type']:
					print "not matching", r, data[r], reaction.attrib['type']
					# for counting reactions with 2 directions
					dup[r] = 0
					# consider reactions with conflicting reversibility to be irreversible
					data[r] = ["irreversible","YES"]
			else:
				data[r] = [reaction.attrib["type"],"NO"]
			# for counting total #
			reac[r] = 0

print "number of inconsistencies", len(dup.keys())
print "total number of reacions", len(reac.keys())

with open('KEGG_Reac.json','w') as f:
	json.dump(data, f)
