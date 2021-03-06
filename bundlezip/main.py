# -*- coding: utf-8 -*-
#Author: zhangguoxin 20190114
import bundle_tarfile
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script') 
    parser.add_argument('--forensics', type=str, default = 'network') 
    parser.add_argument('--start-date', type=int, default=18640101)
    parser.add_argument('--end-date', type=int, default=18640101)
    parser.add_argument('--unit-size', type=str, default='10G') 
    parser.add_argument('--partition-limit', type=float, default=0.9)
    args = parser.parse_args()
    forensics_type = args.forensics
    start_date = args.start_date
    end_date = args.end_date
    unit_size = args.unit_size
    partition_limit = args.partition_limit
    print '\n'
    print '---------------------Start 使用说明 --------------------------------'
    print '1. 直接使用：python main.py' 
    print '默认不加任何参数时，相当于（不做日期过滤）：python main.py --unit-size=10G --forensics=network'
    print '2. 加参数时，使用示例： python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115'
    print '3. 也可以使用重定向输出日志到文件，比如： '
    print '   python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115 > output_log.txt'
    print '4. 如果仅仅预演压缩的结果而不进行实质性压缩，使用以下替换命令后，再运行程序，如：'
    print "   sed -i 's/tar.add/#tar.add/g' bundle_tarfile.py"
    print '\n'
    print '当前参数设置如下：'
    print '  证据文件类型是：%s ，开始时间：%s ， 结束时间：%s ， 压缩文件大小限制： %s 。'% (forensics_type,start_date,end_date,unit_size)
    print '---------------------End 使用说明 --------------------------------\n'
    
    print '---------------------Start 调用Shell脚本--------------------------------'
    var_available_size,du_result_file = bundle_tarfile.collect_du_result(cmd = 'sh du_awk.sh',forensics_type=forensics_type,start_date=start_date,end_date=end_date)
    print '生成%s证据文件目录详细信息的文件位于：%s' % (forensics_type,du_result_file)
    print '当前/var目录可用硬盘空间: %s' % bundle_tarfile.get_str_size(var_available_size*1024)
    print '---------------------End 调用Shell脚本--------------------------------\n'
    #du_result_file='/tmp/network_forensics.txt'
    #du_result_file='forensics_all.txt'
    results = bundle_tarfile.get_du_result(du_result_file)
    #bundle_tarfile.bundle_tar_zip(results, start_date, end_date, unit_size,debug=True,rate=1.0)
    #partition_limit=0.9  #磁盘空间保护：已使用空间超过90%时不压缩证据
    bundle_tarfile.bundle_tar_zip(results,start_date,end_date,unit_size,forensics_type,debug=True,rate=1.0,huge_rate=1.5,buffer_rate=1.25,partition_limit_rate=partition_limit,partition='/var')
    print '---------------------请及时清理备份数据--------------------------------\n'
    print '!!!重要!!!\n!!!重要!!!\n!!!重要!!!\n请及时清理已压缩的证据文件，避免长期占用硬盘空间!!!'
    #the end