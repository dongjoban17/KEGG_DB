'''
Dongjo Ban
Python 2.7
Script for retrieving reaction list for each KEGG genes
'''

import requests
import json
import re
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET

# Extract the list of current reaction ID's
def get_react(gene_reacs):
	
	r_list=[]

	for reac in gene_reacs:
		r_list.append(reac)
	
	return r_list

k = KEGG()
data = dict()
# Create list of hsa pathways
list_path = open("../hsa_list.txt").read().replace('path:','').split('\n')
# Remove newline
list_path.pop()

i = 0
for hsa in list_path:
	i+=1
	print("# of pathways processed: ",i)

	req_url = 'http://rest.kegg.jp/get/'+hsa+'/kgml'
	kmgl = requests.get(req_url)
	root = ET.fromstring(kmgl.text)
	
	for reaction in root.findall("./reaction"): # ALL 'reaction' children of the root
		gene_ids=[]
		gene_names=[]
		subs_list=[]
		prods_list=[]
		# stores reaction ids and their info
		vals={}
		# stores genes and their reactions info
		g_vals={}
		id_look = reaction.attrib["id"] # 'id' to look up in 'graphics' to extract gene name

		for entry in root.findall("./entry"):
			if entry.attrib["id"]==id_look:
				gene_ids = entry.attrib["name"].split(' ')

		r_ids = {}
		for g_id in gene_ids:
			req_reacs = 'http://rest.genome.jp/link/reaction/'+g_id
			req_list = requests.get(req_reacs)
			out = open('reacs/reac_'+g_id,'w')
			for line in req_list.text.splitlines():
				out.write(line)
				out.write('\n')
			out.close()
