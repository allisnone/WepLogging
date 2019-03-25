# bundleZip, Python2.7
#allisnone

该工具用于批量压缩证据文件，基本设计逻辑：以10G为例，做基准
1、按照日期处理和失败证据，以每日为基准分三类：
第一类：单日证据文件非常巨大，比如大于基准的50% --15G，该日分拆压缩：18G，分两个压缩包10G，8G；30G分三个压缩包，以此类推。
第二类： 单日证据文件较大，超过基准，比如10G-15G，直接压缩该日，仅压缩一个压缩包
第三类： 单日证据文件较小，多日合并压缩，按时间排序，每10G压缩一次，每个压缩包不超过10G压缩。
2、脚本分主要分两步：
第一步；通过shell 命令获取证据文件大小和时间信息
第二步： 根据得到以日为单位的证据大小信息，按照上面的分类分别做压缩。

3、默认会做/var目录“爆满”保护，当检测到该目录空间小于10%时，不会在压缩。 如需调整，请改变main.py 中的变量即可：
partition_limit=0.9  #磁盘空间保护：已使用空间超过90%时不压缩证据

4、 使用方法：
将bundlezip.zip上传UCSS目录 /home/skyguardts， 后解压到当前目录
1). 直接使用：python main.py
 默认不加任何参数时，相当于（不做日期过滤）：python main.py --unit-size=10G --forensics=network
2). 加参数时，使用示例： python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115
3). 也可以使用重定向输出日志到文件，便于记录和分析，比如：
   python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115 > output_log.txt
4). 如果仅仅预演压缩的结果而不进行实质性压缩，使用以下替换命令后，再运行程序，如：
	 cp -f bundle_tarfile.py bundle_tarfile_bak.py
   sed -i 's/tar.add/#tar.add/g' bundle_tarfile.py
   默认的原始证据目录和文件大小统计信息，记录文件如下： /tmp/network_forensics.txt
5）. 使用示例：
网络证据备份：
python main.py --unit-size=10G --forensics=network --start-date=20181101 --end-date=20190320  > output_network_log.txt

终端证据备份:
python main.py --unit-size=10G --forensics=endpoint --start-date=20181101 --end-date=20190320  > output_endpoint_log.txt

邮件证据备份：
python main.py --unit-size=10G --forensics=email --start-date=20181101 --end-date=20190320  > output_email_log.txt





