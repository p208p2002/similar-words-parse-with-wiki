import argparse
from Match import KeyMatch
import pickle

# argv
parser = argparse.ArgumentParser(description='similar words with wiki')
parser.add_argument('-s','--start', action="store", dest="start", type=int, required=True)
parser.add_argument('-r','--range', action="store", dest="range", type=int, default=10)
given_args = parser.parse_args()
START = given_args.start
RANGE = given_args.range
print(START,RANGE)

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
fileSn = START
while(True):
    try:
        with open('splitdata/seg_lists_'+str(fileSn)+'.pkl', 'rb') as f:
            data = pickle.load(f)
        fileSn += 1        

        for d in data:
            print(d)
            km.match(keys=d,blackWords=blackWords)
        
        #
        if(fileSn == RANGE):
            print('end@1')
            break            
    except:
        print('end@2')
        break


