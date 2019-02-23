1、先收集信息，默认只收集网络的信息：
 bash du_awk.sh
然后把 /tmp/forensics_all.txt 拷贝出来

2、 收集硬盘和分区信息：
df -k
df -k /var | awk 'END {print $4}'
df -k /var/skyguard/sps/forensics/incident/network | awk 'END {print $4}'

把输出发给出来

3、设定一个时间段先做简单测试