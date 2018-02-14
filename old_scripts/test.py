import json

with open('KEGG_DB.json','r') as fp:
	data=json.load(fp)

print(len(data))