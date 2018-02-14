# Dongjo Ban
# Jordan Lab 2017

import requests
import json
import xml.etree.ElementTree as ET
#from sortedcontainers import SortedDict # optional; sorts the dict 

# data stored and retrieved by gene name
# things to note:
# 1) there could be more than one reaction IDs for a gene entry. however, the reaction type seems to be the same for the reactions
# 2) need to scale up to all human pathways

def get_react(dataset, gene_name):
	r_list=[]
	if gene_name in dataset:
		for i in range(0, len(data[gene_name])):
			r_list.append(data[gene_name][i][0].values()[0])
	return r_list

data = dict()
list_path = open("hsa_list.txt").read().replace('path:','').split('\n') # create list of hsa pathways


kmgl = requests.get('http://rest.kegg.jp/get/hsa00010/kgml')
root = ET.fromstring(kmgl.text)

for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root
	gene_name=""
	subs_list=[]
	prods_list=[]
	vals=[] # stores reaction ID, reaction type, substrates, and products; could be more than one reactions for a gene
	id_look = reaction.attrib["id"] # 'id' to look up in 'graphics' to extract gene name
	r_ids = reaction.attrib["name"].split('rn:') # to iterate through reaction IDs if necessary
	r_type = reaction.attrib["type"] # extracts the reaction type

	for sub in reaction.findall("substrate"):
		subs_list.append(sub.attrib["name"].split(':')[1])

	for prod in reaction.findall("product"):
		prods_list.append(prod.attrib["name"].split(':')[1])

	for entry in root.findall("./entry"):
		if entry.attrib["id"]==id_look:
			gr=entry.find("graphics")
			gene_name = gr.attrib["name"].split(',')[0]
		
	for r_id in r_ids: # handles entries with more than one reaction IDs
		if r_id != '':
			list_check = get_react(data,gene_name)

			if (len(list_check)==0) | (r_id not in list_check) :
				vals.append([{"R_ID": r_id}, {"DIRECTION": r_type}, {"R_SUBS": subs_list}, {"R_PROD": prods_list}])

	if gene_name in data: # if gene already exists, append additional reaction info
		temp = data[gene_name]
		temp.extend(vals)
		data[gene_name] = temp
	else:
		data[gene_name] = vals



with open('KEGG_DB_test1.json','w') as f: # save as .json
	json.dump(data, f)



"""

##############################################################################################
kmgl = requests.get('http://rest.kegg.jp/get/hsa00020/kgml')
root = ET.fromstring(kmgl.text)

for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root
	gene_name=""
	subs_list=[]
	prods_list=[]
	vals=[] # stores reaction ID, reaction type, substrates, and products; could be more than one reactions for a gene
	id_look = reaction.attrib["id"] # 'id' to look up in 'graphics' to extract gene name
	r_ids = reaction.attrib["name"].split('rn:') # to iterate through reaction IDs if necessary
	r_type = reaction.attrib["type"] # extracts the reaction type

	for sub in reaction.findall("substrate"):
		subs_list.append(sub.attrib["name"].split(':')[1])

	for prod in reaction.findall("product"):
		prods_list.append(prod.attrib["name"].split(':')[1])

	for entry in root.findall("./entry"):
		if entry.attrib["id"]==id_look:
			gr=entry.find("graphics")
			gene_name = gr.attrib["name"].split(',')[0]
		
	for r_id in r_ids: # handles entries with more than one reaction IDs
		if r_id != '':
			vals.append([{"R_ID": r_id}, {"DIRECTION": r_type}, {"R_SUBS": subs_list}, {"R_PROD": prods_list}])
			
	if gene_name in data: # if gene already exists, append additional reaction info
		temp = data[gene_name]
		temp.extend(vals)
		data[gene_name] = temp
	else:
		data[gene_name] = vals

with open('KEGG_DB.json','w') as f: # save as .json
	json.dump(data, f)

"""