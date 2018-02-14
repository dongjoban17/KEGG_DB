from bioservices.kegg import KEGG
import json

filename = input('Enter list of KEGG gene identifiers: ')
k = KEGG()
g_kegg = open(filename).read().split('\n')
g_kegg = list(filter(None, g_kegg))
g_list = dict()
for id in g_kegg:
	print(id)
	g_data = k.get(id)
	g_parsed = k.parse(g_data)
	if 'NAME' in g_parsed:
		print(g_parsed['NAME'][0].split(' ')[0].replace(',',''))
		g_list[id] = g_parsed['NAME'][0].split(' ')[0].replace(',','')
	else:
		g_list[id] = 'hsa:'+g_parsed['ENTRY'][0].split(' ')[0].replace(',','')

with open(filename+'.json','w') as j:
	json.dump(g_list,j)
