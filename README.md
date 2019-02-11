# WepLogging
To collect windows endpoint logs including:
1. Agent logs: %promgramfiles%\SkyGuard\SkyGuard Endpoint\EndpointAgent\var\log
2. UCSC SDK logs: %promgramfiles%\SkyGuard\SkyGuard Endpoint\UCSCSDK\var\log
3. APP hook logs: %appdata%\SkyGuard\SkyGuard Endpoint\var\log
4. Installation logs: %temp%\EndpointInstaller.log
5. Running time database: %promgramfiles%\SkyGuard\SkyGuard Endpoint\UCSCSDK\var\
6. Spetial log or config file or dirs.
转化为exe文件：
pyinstaller -F -i 257.ico WepLogs.py
pyinstaller -F -w -i 257.ico WepLogs.py  #忽略console的输出
All logs will output to Desktop:
%userprofile%\desktop\Skyguard_ep_201901026_tar.gz


use following cmd to transfer python to exe:
pyinstaller -F -i 257.ico WepLogs.py

then you can directly run WepLogs.exe in windows OS:
WepLogs.exe -l all

if charset/encoding error(UnicodeEncodeError), run following cmd before run WepLogs.exe:
chcp 65001
set PYTHONIOENCODING=utf-8



WepLogs.exe 使用方法:
1. 获取终端的主要默认日志，包括agent 和 sdk 日志: 直接双击exe文件，或者不加参数直接命令行运行, 日志压缩包位于桌面。有效应用的日志包括：
['agent','sdk','hook','install','specify']
WepLogs.exe 
or WepLogs.exe  -l default
2. 获取全部终端日志，包括 ['agent','sdk','hook','install']
WepLogs.exe  -l all
相当于：
WepLogs.exe  -l agent,sdk,hook,install 

3. 获取多个日志：
WepLogs.exe  -l sdk,hook
WepLogs.exe  -l agent,sdk,hook,install,specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\UCSCSDK\downloads\ep_profile\"

4. 获取额外指定的文件或目录：
WepLogs.exe -l all -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc"
WepLogs.exe -l sdk,specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc"
WepLogs.exe -l specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc"  #仅仅获取额外指定的文件或者目录

5. 仅仅打开sdk DEBUG/TRACE 模式，不收集日志： 通常稍后再收集日志。

WepLogs.exe  -t 0 -d DEBUG
WepLogs.exe  -t 0 -d TRACE

事后需要手动恢复为INFO模式：
WepLogs.exe  -t 0 -d INFO

6. 打开DEBUG日志10分钟后，再收集日志：通常用于用户模拟触发特定场景/事件； -t 参数必须大于0，默认-t参数为-1，表示不等待，只收集日志。
WepLogs.exe  -t 600 -d DEBUG                #开启SDK DEBUG 模式后，等待10分钟，然后收集 sdk, agent日志，收集完日志后恢复INFO模式
WepLogs.exe  -t 600 -d TRACE								#开启SDK TRACE 模式后，等待10分钟，然后收集 sdk, agent日志，收集完日志后恢复INFO模式
WepLogs.exe  -t 600 -d DEBUG	-l all				#开启SDK DEBUG 模式后，等待10分钟，然后收集所有日志，收集完日志后恢复INFO模式

7. 收集日志并上传到SFTP服务器：
python WepLogs.py -f 172.22.80.205 -o 12039 -p 473385fc #上传到sftp服务器默认/tmp目录
python WepLogs.py -f 172.22.80.205 -o 12039 -p 473385fc -e /home/skyguardts/dlplogs #上传到sftp服务器/home/skyguardts/dlplogs目录

WepLogs.exe -f 172.22.80.205 -o 12039 -p 473385fc -e /home/skyguardts/dlplogs

WepLogs.exe  -l agent,sdk,hook,install,specify -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\UCSCSDK\downloads\ep_profile\"  -f 172.22.80.205 -o 12039 -p 473385fc -e /home/skyguardts/dlplogs

