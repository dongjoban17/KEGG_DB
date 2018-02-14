# python(2) script for extracting compounds from KEGG_DB and looking up corresponding names using KEGG from bioservices

import json
from bioservice import KEGG

metab = {}
with open("KEGG_DB.json", "r") as fp:
	data = json.load(fp);

for key, value in data.items():
	for x in value:
		# add substrates
		for y in x[2].values()[0]:
			metab[y] = 0
		# add products
		for z in x[3].values()[0]:
			metab[z] = 0

k = KEGG()
conv = {}
for key in metab:
	ret = k.get(key)
	ret_parsed = k.parse(ret)
	# extract desired info from parsed data
	if 'NAME' in ret_parsed:
		conv[key] = ret_parsed['NAME']
	else: # IDs that start with G's refer to glycan and does not have 'NAME'
		conv[key] = key

with open('cpdNames.json','w') as j:
	json.dump(conv,j)