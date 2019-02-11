# WepLogging
To collect windows endpoint logs including:
1. Agent logs: %promgramfiles%\SkyGuard\SkyGuard Endpoint\EndpointAgent\var\log
2. UCSC SDK logs: %promgramfiles%\SkyGuard\SkyGuard Endpoint\UCSCSDK\var\log
3. APP hook logs: %appdata%\SkyGuard\SkyGuard Endpoint\var\log
4. Installation logs: %temp%\EndpointInstaller.log
5. Running time database: %promgramfiles%\SkyGuard\SkyGuard Endpoint\UCSCSDK\var\
6. Spetial log or config file or dirs.
ת��Ϊexe�ļ���
pyinstaller -F -i 257.ico WepLogs.py
pyinstaller -F -w -i 257.ico WepLogs.py  #����console�����
All logs will output to Desktop:
%userprofile%\desktop\Skyguard_ep_201901026_tar.gz


use following cmd to transfer python to exe:
pyinstaller -F -i 257.ico WepLogs.py

then you can directly run WepLogs.exe in windows OS:
WepLogs.exe -l all

if charset/encoding error(UnicodeEncodeError), run following cmd before run WepLogs.exe:
chcp 65001
set PYTHONIOENCODING=utf-8



WepLogs.exe ʹ�÷���:
1. ��ȡ�ն˵���ҪĬ����־������agent �� sdk ��־: ֱ��˫��exe�ļ������߲��Ӳ���ֱ������������, ��־ѹ����λ�����档��ЧӦ�õ���־������
['agent','sdk','hook','install','specify']
WepLogs.exe 
or WepLogs.exe  -l default
2. ��ȡȫ���ն���־������ ['agent','sdk','hook','install']
WepLogs.exe  -l all
�൱�ڣ�
WepLogs.exe  -l agent,sdk,hook,install 

3. ��ȡ�����־��
WepLogs.exe  -l sdk,hook
WepLogs.exe  -l agent,sdk,hook,install,specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\UCSCSDK\downloads\ep_profile\"

4. ��ȡ����ָ�����ļ���Ŀ¼��
WepLogs.exe -l all -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc"
WepLogs.exe -l sdk,specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc"
WepLogs.exe -l specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc"  #������ȡ����ָ�����ļ�����Ŀ¼

5. ������sdk DEBUG/TRACE ģʽ�����ռ���־�� ͨ���Ժ����ռ���־��

WepLogs.exe  -t 0 -d DEBUG
WepLogs.exe  -t 0 -d TRACE

�º���Ҫ�ֶ��ָ�ΪINFOģʽ��
WepLogs.exe  -t 0 -d INFO

6. ��DEBUG��־10���Ӻ����ռ���־��ͨ�������û�ģ�ⴥ���ض�����/�¼��� -t �����������0��Ĭ��-t����Ϊ-1����ʾ���ȴ���ֻ�ռ���־��
WepLogs.exe  -t 600 -d DEBUG                #����SDK DEBUG ģʽ�󣬵ȴ�10���ӣ�Ȼ���ռ� sdk, agent��־���ռ�����־��ָ�INFOģʽ
WepLogs.exe  -t 600 -d TRACE								#����SDK TRACE ģʽ�󣬵ȴ�10���ӣ�Ȼ���ռ� sdk, agent��־���ռ�����־��ָ�INFOģʽ
WepLogs.exe  -t 600 -d DEBUG	-l all				#����SDK DEBUG ģʽ�󣬵ȴ�10���ӣ�Ȼ���ռ�������־���ռ�����־��ָ�INFOģʽ

7. �ռ���־���ϴ���SFTP��������
python WepLogs.py -f 172.22.80.205 -o 12039 -p 473385fc #�ϴ���sftp������Ĭ��/tmpĿ¼
python WepLogs.py -f 172.22.80.205 -o 12039 -p 473385fc -e /home/skyguardts/dlplogs #�ϴ���sftp������/home/skyguardts/dlplogsĿ¼

WepLogs.exe -f 172.22.80.205 -o 12039 -p 473385fc -e /home/skyguardts/dlplogs

WepLogs.exe  -l agent,sdk,hook,install,specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\UCSCSDK\downloads\ep_profile\"  -f 172.22.80.205 -o 12039 -p 473385fc -e /home/skyguardts/dlplogs

