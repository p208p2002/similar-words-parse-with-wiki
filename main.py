# -!- coding: utf-8 -!-
from KeyMatch import KeyMatch
import pickle
import threading
import time
import re
import argparse

def matchJobThread(matchKey:str,blackWords:list):
    km = KeyMatch() # 初始化
    thread = threading.Thread(target = km.match,args=(matchKey, blackWords, ''))
    thread.start()
    return (thread,km)

def matchKeys(keys:list)->list:
    totalThreads = THREAD
    usingThreads = 0
    jobs = []
    results = []
    for key in keys:
        if(usingThreads < totalThreads):
            t,km = matchJobThread(key, blackWords)
            jobs.append((t,km))
            usingThreads += 1
        else:
            for job in jobs:
                t,km = job
                t.join()
                results.append(km.getTop(SEARCH_RANGE))
                usingThreads -= 1
            jobs = []
    # 如果有尚未跑完的
    if (len(jobs)!=0 ):
        for job in jobs:
            t,km = job
            t.join()
            results.append(km.getTop(SEARCH_RANGE))
    
    return results

def keywordsWithoutTimes(keywords:list):
    newKeywords = []
    for key in keywords:
        k,t = key
        newKeywords.append(k)
    return newKeywords


if __name__ == "__main__":
    # argv
    parser = argparse.ArgumentParser(description='similar words with wiki')
    parser.add_argument('-k','--key', action="store", dest="key", type=str, required=True)
    parser.add_argument('-sr','--search-range', action="store", dest="search_range", type=int, default=25)
    parser.add_argument('-t','--thread', action="store", dest="thread", type=int, default=4)
    given_args = parser.parse_args()
    KEY = given_args.key
    SEARCH_RANGE = given_args.search_range
    THREAD = given_args.thread

    # 自訂單詞黑名單
    with open('blacklists/words.txt','r',encoding='utf-8') as f:
        data = f.read()
    blackWords = data.split()

    # 單詞黑名單字典
    with open('blacklists/words.pkl', 'rb') as f:
        data = list(pickle.load(f))
    blackWords = blackWords + data

    #
    km = KeyMatch()
    matchRes = matchKeys([KEY])[0]

    #
    keys = keywordsWithoutTimes(matchRes)
    print('top keys',keys) # 前10高關鍵字
    keywords = matchKeys(keys) # 找出前10高關鍵字的所有關聯關鍵字
    # print(keywords)

    # 遍歷所有結果，對所有關鍵字再分析
    keywords2 = []
    for kws in keywords:
        key = keywordsWithoutTimes(kws)
        keywords2 = keywords2 + key
            
    keywords2 = list(set(keywords2))
    matchKeys(keywords2)
    
    #
    km = KeyMatch()
    km.match(KEY, blackWords, 'full')
    compareTarget = keywordsWithoutTimes(km.getTop(SEARCH_RANGE))
    commonCounts = []
    compareResults = []
    for kws in keywords2:
        km = KeyMatch()
        km.match(kws, blackWords, 'full')
        kwsMatch = keywordsWithoutTimes(km.getTop(SEARCH_RANGE))
        compareResult = list(set(compareTarget)&set(kwsMatch))
        
        if(len(compareResult)>0):
            compareResults.append((kws,compareResult))
    
    compareResults.sort(key=lambda t: len(t[1]), reverse=True)
    saveFileName = str(int(time.time()))+'.txt'
    onlyKey = []
    for tup in compareResults:
        k,ary = tup
        onlyKey.append(k)
    with open('output/'+saveFileName, 'w',encoding='utf-8') as f:
        outStr = str(onlyKey[0:10])
        outStr = re.sub(r"['\s\[\]']+",'',outStr) # "space" [ ] '
        outStr = outStr.replace(',','\n')
        f.write(outStr)
    
    print('save:','output/'+saveFileName)