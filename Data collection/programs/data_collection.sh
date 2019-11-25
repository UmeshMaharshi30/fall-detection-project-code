activity_name="/a/CC/experiment/Data collection/programs/static_"

for i in 1 2 3 4 5
do
   # lines=$(ps -ef | grep "plink" | wc -l)
   # echo $lines
   echo "start activity"
   sleep 1
   plink -serial COM4 -sercfg 115200,8,1,N,N > "${activity_name}${i}.log"
   PID=`ps -eaf | grep -i "plink" | grep -v grep | awk '{print $2}'`
   echo $PID
   sleep 5
   kill $PID
   echo "data collection successful"
   sleep 5
done