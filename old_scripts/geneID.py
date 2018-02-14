from bioservices.kegg import KEGG

k = KEGG()
g_kegg = open("hsa_gene_list.txt").read().split('\n')
g_list = []
for id in g_kegg:
	print(id)
	g_data = k.get(id)
	g_parsed = k.parse(g_data)
	g_list.append(g_parsed['NAME'][0].split(' ')[0])

print(g_list)
