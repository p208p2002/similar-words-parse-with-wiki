from KeyMatch import KeyMatch
import pickle
import threading

def matchJobThread(matchKey:str,blackWords:list):
    km = KeyMatch() # 初始化
    thread = threading.Thread(target = km.match,args=(matchKey, blackWords, 'full'))
    thread.start()
    return (thread,km)

def matchKeys(keys:list)->list:
    totalThreads = 4
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
                results.append(km.getTop(25))
                usingThreads -= 1
            jobs = []
    # 如果有尚未跑完的
    if (len(jobs)!=0 ):
        for job in jobs:
            t,km = job
            t.join()
            results.append(km.getTop(25))
    
    return results

def keywordsWithoutTimes(keywords:list):
    newKeywords = []
    for key in keywords:
        k,t = key
        newKeywords.append(k)
    return newKeywords


if __name__ == "__main__":
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
    KEY = '華碩'
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
    compareTarget = keywordsWithoutTimes(km.getTop(25))
    commonCounts = []
    compareResults = []
    for kws in keywords2:
        km = KeyMatch()
        km.match(kws, blackWords, 'full')
        kwsMatch = keywordsWithoutTimes(km.getTop(25))
        compareResult = list(set(compareTarget)&set(kwsMatch))
        
        if(len(compareResult)>0):
            compareResults.append((kws,compareResult))
    
    compareResults.sort(key=lambda t: len(t[1]), reverse=False)
    for r in compareResults:
        print(r)

   
        

