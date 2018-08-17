"""
Dongjo Ban
Python 2.7
Script for downloading KEGG gene information
"""

import requests, json, re, sys
from bioservices.kegg import KEGG
import xml.etree.ElementTree as ET

def main():
	# Start KEGG interface
	k = KEGG()
	# Create a dict to store final result
	data = dict()

	# Read in KEGG gene ID & gene symbol pairs
	with open("hsa_gene_list.json","r") as g:
		gene_data = json.load(g)

	for gene in gene_data.keys():
		print gene
		g_data = k.get(gene)
		g_prsd = k.parse(g_data)	
		data[gene] = g_prsd

	with open ('ginfo.json','w') as fw:
		json.dump(data, fw)

if __name__ == "__main__":
	main()
