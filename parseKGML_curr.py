"""#####################################

Dongjo Ban
Jordan Lab 2017
Create KEGG DB for CoMet
Python 2.x

Data is stored and retrieved by gene name

"""######################################

import requests, json, re, sys
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET

# Creates list of reaction IDs
def get_react(gene_reacs):
	r_list=[]
	for reac in gene_reacs:
		r_list.append(reac)
	return r_list

# Retrieves gene names (and aliases) for KEGG IDs
def get_gene(KEGG, gene_ids):
	g_list=[]
	for id in gene_ids:
		# Get initial data from KEGG using ID
		g_data = KEGG.get(id)
		# Parse the information retrieved
		g_parsed = KEGG.parse(g_data)
		if 'NAME' in g_parsed:
			# if NAME key exists, append primary gene symbol and known aliases (if any) to the list
			g_list.append([re.split(', ',g_parsed['NAME'][0])[0], re.split(', ',g_parsed['NAME'][0])[1:]])
		else:
			# Handle cases where an ID does not map to a symbol
			g_list.append('hsa:'+g_parsed['ENTRY'][0].split(' ')[0])
	return g_list

# Retrieves metabolite information from a reaction
def get_metabs(KEGG, reac_id):
	subs_list = []
	prod_list = []
	# Get initial data from KEGG using ID
	r_data = KEGG.get(reac_id)
	# Parse the information retrieved
	r_parsed = KEGG.parse(r_data)
	# Split the equation into substrates and products
	split_eq = re.split('<=>', r_parsed['EQUATION'])
	# Remove the plus signs between the metabolites
	subs_list = [s.strip() for s in split_eq[0].split('+')]
	prod_list = [p.strip() for p in split_eq[1].split('+')]
	return [subs_list, prod_list]

# Debugging class that allows us to output stdout to a log file
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

def main():

	f = open('logfile', 'w')
	backup = sys.stdout
	sys.stdout = Tee(sys.stdout, f)
	# Start KEGG interface
	k = KEGG()
	# Create a dict to store final result
	data = dict()
	# Create list of hsa (human) pathways
	list_path = open("hsa_list.txt").read().replace('path:','').split('\n')
	# Random blank entry removed
	list_path.pop()

	# Read in KEGG gene ID & gene symbol pairs
	with open("hsa_gene_list.json","r") as g:
		gene_data = json.load(g)
	# Read in KEGG reaction ID & reversibility information
	with open("KEGG_Reac.json","r") as fp:
		reac_data = json.load(fp)

	i = 0
	for hsa in list_path:
		i+=1
		print "# of pathways processed: ",i
		# Request KGML file for a pathway
		req_url = 'http://rest.kegg.jp/get/'+hsa+'/kgml'
		kmgl = requests.get(req_url)
		# Construct element tree from the requested info
		root = ET.fromstring(kmgl.text)
		
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
			# Define dict for storing; {gene id: reaction id's}
			r_ids = {}
			# Iterate through the gene IDs to retrieve corresponding list of reaction IDs
			for g_id in gene_ids:
				r_ids[g_id]=[]
				# Parse retrieve reaction information
				# for line in req_list.text.splitlines():
				# 	r_ids[g_id].append(line.split()[1].split('rn:')[1])
				with open('reacs/reac_'+g_id,'r') as rp:
					line = rp.readline()
					while line:
						r_ids[g_id].append(line.split()[1].split('rn:')[1])
						line = rp.readline()

			# Loop to organize into the final output
			for g_id, r_ids in r_ids.items():
				# Stores reaction ids and their info
				vals={}
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

	with open('KEGG_TEST.json','w') as f:
		json.dump(data, f)

if __name__ == "__main__":
	main()