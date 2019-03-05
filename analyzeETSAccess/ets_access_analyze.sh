#!/bin/sh
#Author: zhangguoxin
#Usage: sh ets_access_analyze.sh <ets access file> <outout file>
log=EndpointTrafficServerAccess.log
file=result.txt
#echo $2
if [ $1 ]; then
        log=$1
fi
if [ $2 ]; then
        file=$2
fi
#echo $file
if [ -f $file ]; then
        rm -f $file
fi
echo "---------------- URL access----------------" >> $file
cat $log | gawk -F "URL:" '{print $2}' | gawk -F ']' '{if($0!="") print $1}' | gawk '{a[$1]+=1;} END {for(i in a){print a[i]" "i;}}' |  sort -t " " -k 1 -n -r >> $file
echo "---------------- SERVER access ----------------"  >> $file
cat $log | gawk -F "SERVER:" '{print $2}' | gawk -F ']' '{if($0!="") print $1}' | gawk '{a[$1]+=1;} END {for(i in a){print a[i]" "i;}}' |  sort -t " " -k 1 -n -r >> $file
echo "---------------- PROCNAME access ----------------" >> $file
cat $log | gawk -F "PROCNAME:" '{print $2}' | gawk -F ']' '{if($0!="") print $1}' | gawk '{a[$1]+=1;} END {for(i in a){print a[i]" "i;}}' |  sort -t " " -k 1 -n -r >> $file
echo "---------------- Complete analyze file:  $log ----------------" >> $file
echo "Result file is $file."
exit 1
