import py_classification_cache as pcc
import os
import pickle
pyCahce = pcc.PCC()
files = os.listdir(".kmcache")
for fileName in files:
	try:
		with open('.kmcache/'+ fileName ,'rb') as f:
			data = pickle.load(f)
			fileName = fileName[:-4]        
			pyCahce.save(fileName,data)
	except:
		pass

for fileName in files:
    os.remove('.kmcache/'+ fileName)