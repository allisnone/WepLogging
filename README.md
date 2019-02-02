# WepLogging
To collect windows endpoint logs including:
1. Agent logs: %promgramfiles%\SkyGuard\SkyGuard Endpoint\EndpointAgent\var\log
2. UCSC SDK logs: %promgramfiles%\SkyGuard\SkyGuard Endpoint\UCSCSDK\var\log
3. APP hook logs: %appdata%\SkyGuard\SkyGuard Endpoint\var\log
4. Installation logs: %temp%\EndpointInstaller.log
5. Running time database: %promgramfiles%\SkyGuard\SkyGuard Endpoint\UCSCSDK\var\
6. Spetial log or config file or dirs.
ת��Ϊexe�ļ���
pyinstaller -F -w -i 257.ico WepLogs.py
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
1. ��ȡ�ն˵���ҪĬ����־������agent �� sdk ��־: ֱ��˫��exe�ļ������߲��Ӳ���ֱ������������, ��־ѹ����λ�����档
WepLogs.exe 
or WepLogs.exe  -l default
2. ��ȡȫ���ն���־������ agent, sdk , Installation, app hook
WepLogs.exe  -l all

3. ��ȡ�����־��
WepLogs.exe  -l sdk,hook

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

