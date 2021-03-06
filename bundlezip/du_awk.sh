#!/bin/sh
#Author: zhangguoxin
echo "du_awk.sh 脚本可用参数： \n -f 证据类型：包括email,network,endponit; \n -s 过滤证据的开始时间，如20180821；\n -e 过滤证据的开始时间，如20180821;\n -o 输出的目标文件,如：/tmp/forensics_all.txt。"
echo "\n开始使用awk脚本：默认证据类型是network,无时间过滤。\n"
forensics="network"
start_date=0
end_date=0
out_put=/tmp/network_forensics.txt
echo "du_awk.sh 脚本参数设置："
while getopts ":f:s:e:o:" opt 
do
	case $opt in 
		f) 
		forensics=$OPTARG
		echo "证据类型：$OPTARG" ;;
		s)
		start_date=$OPTARG
		echo "开始日期：$OPTARG" ;;
		e) 
		end_date=$OPTARG
		echo "结束日志：$OPTARG" ;; 
		o) 
		out_put=$OPTARG
		echo "输出目标：$OPTARG" ;;
		?) 
		echo "未知参数" 
		exit 1;; 
	esac
done

#echo $forensics
#echo $start_date
#echo $end_date
#echo $out_put


dir=/var/skyguard/sps/forensics/incident/network/
#时间开始的下标, len($dir)+1
date_index=46

#日期证据的目录长度-1: len($dir) + len(2019/03/23)-2
#du -h max-depth=1 $dir | awk '{if(length($2)>54) {print $2;}}'
#len=date_index+8
len=54
#基于给定的时间过滤
#start_date=20181026
#end_date=20181102

if [ "$forensics" = "endpoint" ]
	then
	#echo "endpoint"
	dir=/var/skyguard/sps/forensics/incident/endpoint/
	date_index=47
	#du -h max-depth=1 $dir | awk '{if(length($2)>55) {print $2;}}'
	len=53
	elif [ "$forensics" = "email" ]
	then
	#echo "email"
	dir=/var/skyguard/sps/forensics/email/
	date_index=35
	len=43
	elif [ "$forensics" = "network" ]
	then
	echo "使用默认证据类型：network"
	else
	echo "指定未知证据类型，退出！请输入正确的证据类型：包括email,network,endponit"
	exit 1
fi

#echo "date_index=$date_index"
#echo "len=$len"
echo "原始证据目录: $dir"
echo "证据文件大小统计文件(du_awk.sh的输出结果): $out_put"

#du -h max-depth=1 $dir | awk '{if(length($2)>11) {split(substr($2,3),a,"/");b=a[1]*10000+a[2]*100+a[3];print $1,$2,substr($2,3),b}}' | sort -t " " -k 4 -n > /tmp/forensics_all.txt
# du -h max-depth=1 $dir | awk -v len="$len" -v date_index="$date_index" '{if(length($2)>len) {split(substr($2,date_index),a,"/");b=a[1]*10000+a[2]*100+a[3];print $1,$2,substr($2,date_index),b}}'

#du -h max-depth=1 $dir | awk -v len="$len" -v date_index="$date_index" -v start_date="$start_date" -v end_date="$end_date" '{if(length($2)>len) {split(substr($2,date_index),a,"/");b=a[1]*10000+a[2]*100+a[3];print $1,$2,substr($2,date_index),b}}'
 
#du -h max-depth=1 $dir | awk -v len="$len" -v date_index="$date_index" -v start_date="$start_date" -v end_date="$end_date" '{if(length($2)>len) {split(substr($2,date_index),a,"/");b=a[1]*10000+a[2]*100+a[3];print $1,$2,substr($2,date_index),b}}' | sort -t " " -k 4 -n > /tmp/forensics_all.txt
du -h max-depth=1 $dir | awk -v len="$len" -v date_index="$date_index" -v start_date="$start_date" -v end_date="$end_date" '{if(length($2)>len) {split(substr($2,date_index),a,"/");b=a[1]*10000+a[2]*100+a[3];result=-1;if(start_date<19000101 && end_date< 19000101){result=1;}else if(start_date>19000101 && end_date< 19000101){if(b>=start_date){result=2;}}else if(start_date<19000101 && end_date> 19000101){if(b<=end_date){result=3;}} else {if(b>=start_date && b<=end_date){result=4;}}if(result>=1){print $1,$2,substr($2,date_index),b;}}}' | sort -t " " -k 4 -n > $out_put