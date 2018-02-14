#####################################################################################
# Remove reversible reactions from KEGG DB
#####################################################################################

import json

data_copy = dict()
# uniq metabs
metab = {}
# metabs with duplicates
metab_dup = []
# uniq metabs
metab2 = {}
metab2_dup= []
gene = []
# flag to check reversibility
rev_flag = False

# import data from JSON
with open("KEGG_DB_Final.json", "r") as fp:
	data = json.load(fp);

for key, value in data.items():
	for x in value:
		# reversibility information 
		if x[1].values()[0] == "reversible":
			rev_flag = True
		# add substrates
		for y in x[2].values()[0]:
			metab[y] = 0
			metab_dup.append(y)
		# add products
		for z in x[3].values()[0]:
			metab[z] = 0
			metab_dup.append(z)
	if rev_flag != True:
		data_copy[key] = value
	#reset flag
	rev_flag = False

for key, value in data_copy.items():
	gene.append(key)
	for x in value:
		# add substrates
		for y in x[2].values()[0]:
			metab2[y] = 0
			metab2_dup.append(y)
		# add products
		for z in x[3].values()[0]:
			metab2[z] = 0
			metab2_dup.append(y)

print "number of genes before removing genes involved in reversible reactions: ", len(data.keys())
print "number of genes after removing genes involved in reversible reactions: ", len(data_copy.keys())
print "number of metabolites before removing metabolites involved in reversible reactions: ", len(metab)
print "number of metabolites after removing metabolites involved in reversible reactions: ", len(metab2)

with open('KEGG_DB_Removed.json','w') as f: # save as .json
	json.dump(data_copy, f)

writefile = open("gene_list.txt", "w")

for x in gene:
	writefile.write("%s\n" %x)

print(len(metab))




