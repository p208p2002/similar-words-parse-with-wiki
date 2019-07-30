# -!- coding: utf-8 -!-
import jieba
import jieba.posseg
# import jieba.analyse
import json
import os
from collections import Counter
import pickle
import copy
import py_classification_cache as pcc

class KeyMatch():
    def __init__(self):        
        self.keyMatchRes = []
        self.pyCache = pcc.PCC('.kmcache')
            
    def match(self, keys=[], blackWords=[]):        
        self.__matchKey(keys, blackWords)
    
    def loadWiki(self,subDir=''):
        fileSN = 0
        fileBaseName = 'seg_lists_'
        fileRootPath = 'splitdata/' + subDir 
        jsonDataAsWords = [] # 讀入的資料存檔        
        print('load wiki')
        with open(fileRootPath + '/' + fileBaseName + str(fileSN) + '.pkl', 'rb') as f:
            self.jsonDataAsWords = pickle.load(f)
        print('finish')

    
    def __matchKey(self, keys, blackWords=[]):
        keysB = copy.copy(keys)
        keyMatchRes = {} # 與關鍵字匹配
        for key in keysB:                        
            if(self.pyCache.get(key) != None):
                # print(key,'快取存在')
                keys.remove(key)
        if(len(keys)>0):
            # print("搜尋:",keys)
            jsonDataAsWords = self.jsonDataAsWords

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
            
            # 儲存快取檔案
            if(len(keys)>0):                
                for key in keyMatchRes:
                    print('建立快取:',key)
                    self.pyCache.save(key,keyMatchRes[key])