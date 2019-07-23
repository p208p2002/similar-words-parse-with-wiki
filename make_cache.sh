#!/bin/sh
# chmod 755 make_cache.sh 
echo "*make cache*"
echo "check running: ps -ef | grep make_cache.py"
echo "stop program: kill PID"
# exec pipenv shell
# echo $(($i*100+200))
for i in 0 2 4 6 8 10 12 14 16 18 20 22 24
do
    exec nohup python make_cache.py -s=$(($i*100)) -r=200 &
done
