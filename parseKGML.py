"""
Dongjo Ban
Python 2.7
Script for generating metabolic network (JSON) from KEGG
"""

import requests, json, re, sys
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET

# Function to create list of KEGG reaction IDs
def get_react(gene_reacs):
	r_list=[]
	
	for reac in gene_reacs:
		r_list.append(reac)
	
	return r_list

# Function to retrieve metabolite information from a reaction
def get_metabs(KEGG, reac_id):
	subs_list = []
	prod_list = []

	# Get reaction data from KEGG using a KEGG reaction ID
	r_data = KEGG.get(reac_id)
	# Parse the information retrieved
	r_parsed = KEGG.parse(r_data)
	# Split the equation into substrates and products
	split_eq = re.split('<=>', r_parsed['EQUATION'])
	# Remove the plus signs between the metabolites
	subs_list = [s.strip() for s in split_eq[0].split('+')]
	prod_list = [p.strip() for p in split_eq[1].split('+')]

	return [subs_list, prod_list]

def main():
	# Start KEGG interface for querying
	k = KEGG()
	# Create a dict to store final network output
	data = dict()
	# Create list of hsa (human) pathways
	list_path = open("hsa_list.txt").read().replace('path:','').split('\n')
	# Remove newline
	list_path.pop()

	# Read in KEGG reaction ID & reversibility information
	with open("KEGG_Reac.json","r") as fp:
		reac_data = json.load(fp)
	
	# Read in KEGG gene data
	with open("ginfo.json","r") as fp2:
		gene_data = json.load(fp2)

	# Keep track of # of pathways processed
	i = 0
	for hsa in list_path:		
		i+=1
		print "# of pathways processed: ", i
		# Open previously extracted KGML files
		kgml = open("etc_scripts/KEGG_DB_PATH/pathways/path_"+hsa).read()
		# Construct element tree
		root = ET.fromstring(kgml)
		
		# Iterate through ALL reactions
		for reaction in root.findall("./reaction"):
			gene_ids=[]
			gene_names=[]
			subs_list=[]
			prods_list=[]
			# 'id' to look up in 'graphics' to extract gene name
			id_look = reaction.attrib["id"]
			# Iterate through 'entry' to retrieve gene IDs
			for entry in root.findall("./entry"):
				if entry.attrib["id"]==id_look:
					gene_ids = entry.attrib["name"].split(' ')
			# Define dict for storing {gene id: reaction id's}
			r_ids = dict()
			# Iterate through the gene IDs to retrieve corresponding list of reaction IDs
			for g_id in gene_ids:
				r_ids[g_id]=[]
				# Open previously extracted reaction information
				with open('reacs/reac_'+g_id,'r') as rp:
					line = rp.readline()
					# With gene ids as key, store corresponding reaction ids
					while line:
						r_ids[g_id].append(line.split()[1].split('rn:')[1])
						line = rp.readline()

			# Loop to organize into the final output
			for g_id, r_ids in r_ids.items():
				# Stores reaction ids and their info
				vals=dict()
				# Iterate through list of reactions to get metabolite information
				for r_id in r_ids:
					# Get the list of substrates and products
					metabs = get_metabs(k, r_id)
					# Check if reaction exists in reaction DB
					if r_id in reac_data.keys():
						r_type = reac_data[r_id]
					else:
						# If it doesn't exist, assign NA as direction
						r_type = "NA"
					# Intermediate result to add to a gene of the current loop iteration
					vals[r_id] = {"DIRECTION": r_type, "R_SUBS": metabs[0], "R_PROD": metabs[1]} 

				# Check to see if the gene has been encountered previously
				if g_id in data:
					# Store the current info to a temp reaction information
					temp = data[g_id]
					# Retrieve the current reaction information for the gene
					temp_list = get_react(temp)
					# Iterate through the existing information on reaction...
					# If a new reaction is seen, it is added to temp reaction information
					for r in vals.keys():
						if r not in temp_list:
							temp[r] = vals[r]
					# Finalize reaction information to be added to the gene
					data[g_id] = temp
				else:
					data[g_id] = vals

	with open('keggMetabNetwork.json','w') as f:
		json.dump(data, f)

if __name__ == "__main__":
	main()
