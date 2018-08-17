"""
Dongjo Ban
Python 2.7
Script for downloading KGML associated with human pathways
"""

import requests, json, re, sys
from bioservices.kegg import KEGG

def main():
	k = KEGG()
	# Create a dict to store final result
	data = dict()
	# Create list of hsa (human) pathways
	list_path = open("../hsa_list.txt").read().replace('path:','').split('\n')
	# Random blank entry removed
	list_path.pop()

	i = 0
	for hsa in list_path:
		i+=1
		print "# of pathways processed: ",i
		# Request KGML file for a pathway
		req_url = 'http://rest.kegg.jp/get/'+hsa+'/kgml'
		kgml = requests.get(req_url)
		out = open('pathways/path_'+hsa,'w')
		out.write(kgml.text)
		out.close()

if __name__ == "__main__":
	main()
