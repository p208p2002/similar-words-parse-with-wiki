from KeyMatch import KeyMatch
import pickle
import threading
import argparse

def matchJobThread(matchKey:str,blackWords:list):
    km = KeyMatch() # 初始化
    thread = threading.Thread(target = km.match,args=(matchKey, blackWords))
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
                results.append(km.getTop(0))
                usingThreads -= 1
            jobs = []
    # 如果有尚未跑完的
    if (len(jobs)!=0 ):
        for job in jobs:
            t,km = job
            t.join()
            results.append(km.getTop(0))
    
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
    parser.add_argument('-t','--thread', action="store", dest="thread", type=int, default=4)
    given_args = parser.parse_args()
    THREAD = given_args.thread

    # 自訂單詞黑名單
    with open('blacklists/words.txt','r',encoding='utf-8') as f:
        data = f.read()
    blackWords = data.split()

    # 單詞黑名單字典
    with open('blacklists/words.pkl', 'rb') as f:
        data = list(pickle.load(f))
    blackWords = blackWords + data

    fileSn = 0
    while(True):
        try:
            with open('splitdata/seg_lists_'+str(fileSn)+'.pkl', 'rb') as f:
                data = pickle.load(f)
            fileSn += 1

            for d in data:
                print(d)
                matchKeys(d)
        except:
            print('end')
            break
    
    