# import argparse
from core.MuiltMatch import KeyMatch
import pickle
from multiprocessing import Process

# argv
# parser = argparse.ArgumentParser(description='similar words with wiki')
# parser.add_argument('-t','--thread', action="store", dest="thread", type=int, default=4)
# given_args = parser.parse_args()
# THREAD = given_args.thread

KM = KeyMatch() # 初始化
KM.loadWiki(subDir='big')

def matchThread(start,range):
    START = start
    RANGE = range
    # 自訂單詞黑名單
    with open('blacklists/words.txt','r',encoding='utf-8') as f:
        data = f.read()
    blackWords = data.split()

    # 單詞黑名單字典
    with open('blacklists/words.pkl', 'rb') as f:
        data = list(pickle.load(f))
    blackWords = blackWords + data

    #
    fileSn = START
    while(True):
        try:
            with open('splitdata/seg_lists_'+str(fileSn)+'.pkl', 'rb') as f:
                data = pickle.load(f)
            fileSn += 1        

            for d in data:
                # print(d)
                KM.match(keys=d,blackWords=blackWords)
            
            #
            if(fileSn == RANGE):
                print('end@1')
                break            
        except:
            print('end@2')
            break

SPLIT_TOTAL = 2458
THREAD = 8
RANGE = int(SPLIT_TOTAL/THREAD)+1
s = 0
threads = []
for i in range(THREAD):
    thread = Process(target = matchThread,args=(s,RANGE))
    thread.start()
    threads.append(thread)
    # print(s,RANGE+s,RANGE)
    s+=RANGE
    

for t in threads:
    t.join()


