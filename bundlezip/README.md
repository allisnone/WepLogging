# bundleZip, Python2.7
#allisnone

�ù�����������ѹ��֤���ļ�����������߼�����10GΪ��������׼
1���������ڴ����ʧ��֤�ݣ���ÿ��Ϊ��׼�����ࣺ
��һ�ࣺ����֤���ļ��ǳ��޴󣬱�����ڻ�׼��50% --15G�����շֲ�ѹ����18G��������ѹ����10G��8G��30G������ѹ�������Դ����ơ�
�ڶ��ࣺ ����֤���ļ��ϴ󣬳�����׼������10G-15G��ֱ��ѹ�����գ���ѹ��һ��ѹ����
�����ࣺ ����֤���ļ���С�����պϲ�ѹ������ʱ������ÿ10Gѹ��һ�Σ�ÿ��ѹ����������10Gѹ����
2���ű�����Ҫ��������
��һ����ͨ��shell �����ȡ֤���ļ���С��ʱ����Ϣ
�ڶ����� ���ݵõ�����Ϊ��λ��֤�ݴ�С��Ϣ����������ķ���ֱ���ѹ����

3��Ĭ�ϻ���/varĿ¼������������������⵽��Ŀ¼�ռ�С��10%ʱ��������ѹ���� �����������ı�main.py �еı������ɣ�
partition_limit=0.9  #���̿ռ䱣������ʹ�ÿռ䳬��90%ʱ��ѹ��֤��

4�� ʹ�÷�����
��bundlezip.zip�ϴ�UCSSĿ¼ /home/skyguardts�� ���ѹ����ǰĿ¼
1). ֱ��ʹ�ã�python main.py
 Ĭ�ϲ����κβ���ʱ���൱�ڣ��������ڹ��ˣ���python main.py --unit-size=10G --forensics=network
2). �Ӳ���ʱ��ʹ��ʾ���� python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115
3). Ҳ����ʹ���ض��������־���ļ������ڼ�¼�ͷ��������磺
   python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115 > output_log.txt
4). �������Ԥ��ѹ���Ľ����������ʵ����ѹ����ʹ�������滻����������г����磺
	 cp -f bundle_tarfile.py bundle_tarfile_bak.py
   sed -i 's/tar.add/#tar.add/g' bundle_tarfile.py
   Ĭ�ϵ�ԭʼ֤��Ŀ¼���ļ���Сͳ����Ϣ����¼�ļ����£� /tmp/network_forensics.txt
5��. ʹ��ʾ����
����֤�ݱ��ݣ�
python main.py --unit-size=10G --forensics=network --start-date=20181101 --end-date=20190320  > output_network_log.txt

�ն�֤�ݱ���:
python main.py --unit-size=10G --forensics=endpoint --start-date=20181101 --end-date=20190320  > output_endpoint_log.txt

�ʼ�֤�ݱ��ݣ�
python main.py --unit-size=10G --forensics=email --start-date=20181101 --end-date=20190320  > output_email_log.txt





