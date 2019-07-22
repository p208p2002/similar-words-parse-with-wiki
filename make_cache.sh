#!/bin/sh
# chmod 755 make_cache.sh 
echo "*make cache*"
echo "check running: ps -ef | grep nohup python make_cache.py"
echo "stop program: kill PID"
# exec pipenv shell
for i in 0 400 800 1200 1600 2000 2400
do
   exec nohup python make_cache.py -s=$i -r=400 &
done
