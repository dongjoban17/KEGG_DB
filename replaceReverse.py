# python 2

import json

with open('KEGG_Reac.json','r') as fp1:
	reverseList = json.load(fp1)

with open('KEGG_DB_FEB16.json','r') as fp2:
	updateDB = json.load(fp2)

data = dict()
for reac in reverseList.keys():
	for gene, info in updateDB.items():
		for key in info.keys():
			if key != 'ALIAS':
				info[key]["CONFLICT"] = "NA"

		if reac in info.keys():
			info[reac]['DIRECTION'] = reverseList[reac][0]
			info[reac]['CONFLICT'] = reverseList[reac][1]
			data[gene] = info
		else:
			data[gene] = info

with open('test1.json','w') as wf:
	json.dump(data, wf)
