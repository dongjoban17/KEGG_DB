import json
import re
from bioservices import KEGG

def main():

	with open("Test_DB.json") as kg:
		kegg_data = json.load(kg)

	k = KEGG()

	temp_dict = {}
	for key, val in kegg_data.items():
		print key

		ret_data = k.get(key)
		prs_data = k.parse(ret_data)

		if "NAME" in prs_data:
			gene_names = [re.split(', ',prs_data['NAME'][0])[0], re.split(', ',prs_data['NAME'][0])[1:]]
		else:
			gene_names = [key, []]

		val['ALIAS'] = gene_names[1]
		temp_dict[gene_names[0]] = val

	with open("KEGG_DB_FIN.json","w") as fw:
		json.dump(temp_dict, fw)

if __name__ == "__main__":
	main()