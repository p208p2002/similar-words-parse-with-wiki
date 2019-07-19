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
                results.append(km.getTop(10))
                usingThreads -= 1
            jobs = []
    # 如果有尚未跑完的
    if (len(jobs)!=0 ):
        for job in jobs:
            t,km = job
            t.join()
            results.append(km.getTop(10))
    
    return results

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
    key = '陳水扁'
    km.match(key, blackWords, 'full')
    matchRes = km.getTop(10)
    
    #
    keys = []
    for res in matchRes:
        key, times = res
        keys.append(key)
    
    print('top keys',keys)

    results = matchKeys(keys)
    
    print('ok')
    for r in results:
        print(r)

