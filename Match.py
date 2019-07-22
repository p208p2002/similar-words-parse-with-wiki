# -!- coding: utf-8 -!-
import jieba
import jieba.posseg
# import jieba.analyse
import json
import os
from collections import Counter
import pickle
import copy

class KeyMatch():
    def __init__(self):        
        self.keyMatchRes = []
            
    def match(self, keys=[], blackWords=[], subDir= ''):        
        self.__matchKey(keys, blackWords, subDir)
    
    def __matchKey(self, keys, blackWords=[], subDir= ''):
        keysB = copy.copy(keys)
        for key in keysB:            
            if os.path.exists('.kmcache/'+key+'.pkl'):
                print(key,'快取存在')
                keys.remove(key)          
        if(len(keys)>0):
            print("搜尋:",keys)
            fileSN = 0
            totalFiles = 0
            fileBaseName = 'seg_lists_'
            fileRootPath = 'splitdata/' + subDir 
            jsonDataAsWords = [] # 讀入的資料存檔        
            keyMatchRes = {} # 與關鍵字匹配

            # 檢測檔案數量
            while(True):
                if os.path.isfile(fileRootPath + '/' + fileBaseName+str(totalFiles) + '.pkl'):
                    totalFiles += 1
                else:                
                    totalFiles -= 1                
                    break        

            # 讀入存檔資料
            while(True):            
                try:
                    with open(fileRootPath + '/' + fileBaseName + str(fileSN) + '.pkl', 'rb') as f:
                        jsonDataAsWords = pickle.load(f)
                    # print('matching:',str(fileSN) + '/' + str(totalFiles))
                    fileSN += 1
                    
                    # 匹配關鍵字                
                    for words in jsonDataAsWords:
                        for key in keys:
                            if key in words:
                                for i in words:
                                    if (i != key) and (not i in blackWords) and i != ' ':
                                        kmrKey = keyMatchRes.get(key)
                                        if(kmrKey == None):
                                            keyMatchRes[key]={}
                                        keyVal = keyMatchRes[key].get(i)
                                        if(keyVal == None):
                                            keyMatchRes[key][i] = 1
                                        else:
                                            keyVal += 1
                                            keyMatchRes[key][i] = keyVal
                            else:
                                continue
                    del jsonDataAsWords                

                except:                
                    break
            
            # 儲存快取檔案
            if(len(keys)>0):                
                for key in keyMatchRes:
                    print('建立快取:',key)
                    with open('.kmcache/'+ key +'.pkl','wb') as f:
                        pickle.dump(keyMatchRes[key],f)
            
            # print(keyMatchRes)
            # self.keyMatchRes = keyMatchRes
