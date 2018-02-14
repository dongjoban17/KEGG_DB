# Dongjo Ban
# Jordan Lab 2017
# Create KEGG DB for CoMet

import requests
import json
import re
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET
import sys # DEBUGGING
#from sortedcontainers import SortedDict # optional; sorts the dict 

# data stored and retrieved by gene name
# things to note:
# 1) there could be more than one reaction IDs for a gene entry. however, the reaction type seems to be the same for the reactions

def get_react(gene_reacs): # extract the list of current reaction ID's
	
	r_list=[]

	for reac in gene_reacs:
		r_list.append(reac['R_ID'])
	
	return r_list

def get_gene(KEGG, gene_ids):
	
	g_list=[]

	for id in gene_ids:
#		print(id)
		g_data = KEGG.get(id)
		g_parsed = KEGG.parse(g_data)
		if 'NAME' in g_parsed:
			g_list.append(g_parsed['NAME'][0].split(' ')[0].split(',')[0])
		else:
			g_list.append('hsa:'+g_parsed['ENTRY'][0].split(' ')[0]) # for genes without names in KEGG

	return g_list
k=KEGG()
data = dict()

req_url = 'http://rest.kegg.jp/get/hsa00970/kgml'
# print "\n########pathway being processed >>> ", hsa, "\n"
kmgl = requests.get(req_url)
root = ET.fromstring(kmgl.text)
name_clean = re.compile('[^a-zA-Z0-9]')
metab_split = re.compile('[a-z]+:[A-Z0-9]+')
for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root
	gene_ids=[]
	gene_names=[]
	subs_list=[]
	prods_list=[]
	vals=[] # stores reaction ID, reaction type, substrates, and products; could be more than one reactions for a gene
	id_look = reaction.attrib["id"] # 'id' to look up in 'graphics' to extract gene name
	r_ids = reaction.attrib["name"].split('rn:') # to iterate through reaction IDs if necessary
	r_type = reaction.attrib["type"] # extracts the reaction type

	for sub in reaction.findall("substrate"):
			#subs_list.append(sub.attrib["name"].split(':')[1]) #[old code]
		subs_list += metab_split.findall(sub.attrib["name"])

	for prod in reaction.findall("product"):
			#prods_list.append(prod.attrib["name"].split(':')[1]) #[old code]
		prods_list += metab_split.findall(prod.attrib["name"])

	for entry in root.findall("./entry"):
		if entry.attrib["id"]==id_look:
			gene_ids = entry.attrib["name"].split(' ')
			# get all known aliases for a gene
			gene_names = get_gene(k, gene_ids)
			print gene_names
	# handles entries with more than one reaction IDs, but same substrate & product
	for r_id in r_ids: 
		if r_id != '':
			vals.append([{"R_ID": r_id, "DIRECTION": r_type, "R_SUBS": subs_list, "R_PROD": prods_list}])
	# set alias to all but first occuring gene symbol
	name = gene_names[0]
	alias = [{"ALIAS": [x.encode('utf-8') for x in gene_names[1:]]}]
	# check to see if gene already exists in dict
	if name in data:
		# get current info for the gene
		temp = data[name]
		print "this is temp[1]", temp[1]
		# create a temporary list of reactions present in current info
		temp_list = get_react(temp[1])
		# check info to-be-added to see if it contains reaction already present in current info
		for r in vals:
			if r[0]['R_ID'] not in temp_list:
				temp.append(r)
			data[name] = temp
	else:
		data[name] = alias+vals

print data

# with open('2_8.json','w') as f: # save as .json
# 	json.dump(data, f)