import json

with open('KEGG_DB_all_hsa.json','r') as fp:
	data=json.load(fp)

print(len(data))