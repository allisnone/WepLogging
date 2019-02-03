# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-01-26
import argparse
import importlib
import sys
import tarfile
import time
import os
import paramiko
import shutil

class WepLogCollection:
    """
    用于收集终端的日志
    """
    def __init__(self, ep_version='v2.3.0',types='',specify='',debug=False,timer=300):
        self.ep_version = ep_version
        self.log_types = []
        self.sdk_debug = debug
        self.timer = timer
        self.specify = specify
        self.valid_versions = ['v2.3,.0', 'v2.2.0']
        self.log_dir_data = {}
        self.output_logs = ''
        self.initial_dlp_logs(types,specify,debug)
        
    def initial_dlp_logs(self,types,specify,debug):
        self.set_log_types(types)
        if self.log_types:
            self.set_specify(specify) #设置特殊目录日志
            self.set_all_version_datas()
            self.output_logs = self.tar_dlp_log_files(self.get_version_data())
        else:
            self.set_sdklog_level(debug)
            self.restore_log_level()
        return    
    
    def get_agent_version(self): 
        return       
    
    def set_valid_agent_versions(self,versions=[]):
        self.valid_versions = versions
        return
    
    def set_agent_version(self,version='v2.3.0'):
        self.ep_version = version.lower()
        return
    
    def is_valid_ep_version(self,version=''):
        """
        判断是否是有效的终端版本，v2.3.0,V2.3.0,v2.3,V2.3,v2,v3
        """
        ver = self.ep_version
        if version: 
            ver = version
        if ver and isinstance(ver,str):
            if 'v' not in ver:
                ver = 'v' + ver
            if len(ver.split('.'))==1:
                ver = ver + '.0'
            elif len(ver.split('.'))==0:
                ver = ver + '.0.0'
            else:
                pass
        else:
            return False
        return ver.lower() in list(self.all_version_datas.keys())
    
    def set_specify(self,specify=''):
        """
        设置特定目录
        """
        if specify:
            self.specify = specify
        else:
            pass
        return
    
    def set_log_types(self,types=''):
        """
        设置要收集的日志类型，如果需要收集特殊日志或者配置文件，参数specify必须非空
        :parama types: str or list type
        """
        valid_log_types = ['agent','sdk','hook','install','specify']
        default_type_list = ['agent','sdk','install']
        if types:
            pass
        else:#默认只取agent和sdk的日志
            self.log_types = default_type_list
            return 
        if isinstance(types,str): #一种类型
            if types in valid_log_types:
                self.log_types = [type]
            elif types=='default': #默认只取agent和sdk的日志
                self.log_types = default_type_list
            elif types=='all': #收取全部日志
                self.log_types = valid_log_types
            else:
                print('ERROR：输入无效的日志类型：%s' % types)
        elif isinstance(types, list): #给定多种类型，list    
            default_types = list(set(['default','all']).intersection(set(types)))
            if len(default_types)==0: #无all或default 类型
                self.log_types = list(set(valid_log_types).intersection(set(types)))
                invalid_log_types = list(set(types).difference(set(valid_log_types)))
                if invalid_log_types: #判断是否有无效的数据类型
                    print('ERROR-输入无效的多种日志类型：%s' % invalid_log_types)
            elif len(default_types)==1: #含all或default 类型之一
                if 'all' in types:
                    self.log_types = valid_log_types
                else: #'default' in types:
                    self.log_types = list(set(valid_log_types).intersection(set(types + default_type_list)))
            else:
                print('ERROR： default和all类型不能同时选择！')
        else:
            print('ERROR-输入其他无效的日志类型：%s，请确保数日str或者是list类型！' % type(types))
        return
    
    def set_all_version_datas(self,datas={}):
        """
        设置各版本要收集的日志目录或者文件
        """
        v23_datas = {
                'agent': 'PROGRAMW6432_SkyGuard\SkyGuard Endpoint\EndpointAgent\\var\\log\\',
                'sdk': 'PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\log\\',
                'hook': 'APPDATA_SkyGuard\SkyGuard Endpoint\\var\\log\\',
                'install': 'TEMP_EndpointInstaller.log',
                'sdkdb': '%PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\cache\\',
                'specify': ''
                }
        self.all_version_datas = {
            'v3.0.0': v23_datas,
            'v2.3.0': v23_datas,
            'v2.2.0':{
                'agent': 'PROGRAMW6432_SkyGuard\SkyGuard Endpoint\EndpointAgent\\var\\log\\',
                'sdk': 'PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\log\\',
                'hook': 'APPDATA_SkyGuard\SkyGuard Endpoint\\var\\log\\',
                'install': 'TEMP_EndpointInstaller.log',
                'sdkdb': 'PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\cache\\',
                'specify': ''
                },   
            }
        if datas:
            self.all_version_datas = datas
        return
            
    def get_version_data(self):
        """
        获取要收集的该终端的目录/文件信息
        """
        if self.is_valid_ep_version():
            log_dir_data = self.all_version_datas[self.ep_version]
            #print('log_dir_data=',log_dir_data)
            all_this_version_types = list(log_dir_data.keys())
            except_logs_types = list(set(all_this_version_types).difference(self.log_types))
            if except_logs_types: #收集已定义日志类型中的一部分
                for type in except_logs_types: #如果在例外，则置空
                    log_dir_data[type] = ''
            else:#全部收集
                pass
            if self.specify:
                log_dir_data['specify'] = self.specify
            else:
                pass
            #print('log_dir_data=',log_dir_data)
            return log_dir_data
        else:
            print('ERROR：请设置正确的ep_version或更新all_version_datas！')
            return {} 
        
    def tar_dlp_log_files(self,log_dir_data):
        """
        根据参数设置sdk 日志level，并收集日志，打包压缩
        :return: 打包压缩的文件名
        """
        full_tar_dlp_log_files_name = ''
        is_switch_sdk_log_level = False
        if self.sdk_debug in ['DEBUG', 'TRACE']:
            #DEBUG或者TRACE模式时，设置SDK 的log level
            is_switch_sdk_log_level = True
            if self.timer>0: #DEBUG或者Trace模式，同时时间大于0时，等待若干秒
                self.set_sdklog_level()
                print('已开启SDK日志模式: %s, 将等待%s秒后自动收集日志...' % (self.sdk_debug,self.timer))
                time.sleep(self.timer)
            elif self.timer==0:  #仅开启DEBUG或者TRACE模式，且不收集日志
                self.set_sdklog_level()
                print('仅开启SDK日志模式: %s' % self.sdk_debug)
                return ''
            else:#小于0的整数，仅仅收集日志
                pass
        if log_dir_data:
            date_str = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
            #print os.environ 
            #print os.getenv('PROGRAMW6432')
            user_path = os.path.expanduser("~")
            desktop_dir = os.path.join(user_path, 'Desktop')
            tar_dlp_log_files_name = 'skydlp_' + user_path.split('\\')[-1] + '_'  + date_str + '.tar.gz'
            full_tar_dlp_log_files_name = os.path.join(desktop_dir,tar_dlp_log_files_name)
            print('full_tar_dlp_log_files_name=',full_tar_dlp_log_files_name)
            tar_obj = tarfile.open(full_tar_dlp_log_files_name,'w:gz')
            #获取字典中非空的数据
            log_dir_data = {k: v for k, v in log_dir_data.items() if v}
            log_dirs = []
            for k, v in log_dir_data.items():
                log_dirs.append(v)
                if k =='install':
                    log_dirs.append('TEMP_EndpointInstaller1.log')
                    log_dirs.append('TEMP_EndpointInstaller2.log')
                else:
                    pass
            #log_dirs = [v for k, v in log_dir_data.items() if v]
            profix_dirs = ['PROGRAMW6432_','APPDATA_','TEMP_']
            for dir in log_dirs:
                
                is_spectial_head = False
                for profix in profix_dirs:
                    if profix in dir:
                        dirs = dir.split('_')
                        is_spectial_head = True
                        this_dir = os.path.join(os.getenv(dirs[0]),dirs[1])
                        if this_dir and os.path.exists(this_dir):
                            tar_obj.add(this_dir) 
                            break
                        else:
                            print('Warning: 文件或目录不存在，请检查终端是否已安装：%s' % this_dir)
                    else:
                        pass
                #print('dir=',dir,is_spectial_head)
                if not is_spectial_head:
                    if dir and os.path.exists(dir):
                            tar_obj.add(dir) 
                    else:
                        print('Warning: 文件或者目录不存在，请检查终端是否已安装1：%s' % dir)
            tar_obj.close()
        if is_switch_sdk_log_level and self.timer>0:
            self.restore_log_level()
        return full_tar_dlp_log_files_name
    
    def set_sdklog_level(self,level=''):
        """
        设置sdk日志级别，返回是否切换成功
        """
        if not level:
            level = self.sdk_debug
        sdk_util = os.path.join(os.getenv('PROGRAMW6432'),'SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\bin\\ucsc_util.exe')
        is_swtich_successful = False
        if os.path.exists(sdk_util):
            if level.upper() in ['INFO', 'DEBUG', 'TRACE']:
                cmd = '"%s"' % sdk_util+ ' --logging_level %s' % level.upper()
                result = os.popen(cmd).readlines()
                for res in result:
                    if 'successful' in res: 
                        is_swtich_successful = True
                        break
                if is_swtich_successful:
                    print('成功开启或切换SDK日志为"%s"模式！' % level)
                else:
                    print('ERROR: 切换SDK日志%s模式失败！ %s' % (level,result))
            else:
                print('ERROR: 不存在该SDK日志模式%s' % level)
        else:
            print('Warning: 文件不存在%s' % sdk_util)
        return is_swtich_successful
    
    def restore_log_level(self,force=False):
        """
        恢复SDK日志级别为INFO
        """
        if force:
            self.set_sdklog_level(level='INFO')
            return 
        if self.sdk_debug in ['DEBUG', 'TRACE']:
            self.set_sdklog_level(level='INFO')
            print('已恢复SDK日志为INFO模式！')
        return
    
class SftpClient:
    #sftp 上传或者下载文件
    def __init__(self,ip,port=22,username='skygardts',password='123456',private_key_file=''):
        self.transport = None
        self.sftp = None
        self.set_sftp_connection(ip,port,username=username,password=password,private_key_file=private_key_file)
        
    def set_sftp_connection(self,ip,port=22,username='username',password='123456',private_key_file=''):
        #初始化sftp的连接
        self.transport = paramiko.Transport((ip, port))
        if private_key_file:
            self.transport.connect(username=username, pkey=private_key)
        else:
            self.transport.connect(username=username, password=passwd)
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        return
        
    def _put(self,source,dest):
        # sftp 上传文件
        return self.sftp.put(source, dest)
    
    def put(self,source,dest):
        self._put(source, dest)
        self.close()
        return
    
    def _get(self,source,dest):
        #sftp 下载文件
        return self.sftp.get(source, dest)
    
    def get(self,source,dest):
        self._get(source, dest)
        self.close()
        return 
        
    def close(self):
        return self.transport.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script') 
    parser.add_argument('-v','--version', type=str, default = 'v2.3.0',help='指定需收集日志的终端的版本，格式如v2.3.0') 
    parser.add_argument('-l','--log-types', type=str, default= 'default',help='收集终端模块的日志类型，有效类型：all（除specify以外的所有类型）, defualt（agent,sdk两种）, 或[agent,sdk,hook,install,specify]的任意组合-需以英文逗号分隔。')
    parser.add_argument('-d','--debug', type=str, default='INFO',help='是否开启或者切换SDK日志level，有效level为: INFO, DEBUG, TRACE；其他输入为无效，不改变sdk的日志模式。')
    parser.add_argument('-t','--time', type=int, default=-1,help='先切换SDK的日志模式，等待若干秒后，再收集日志，与-d DEBUG（或TRACE）参数组合使用；通常用于收集特定场景的日志。') 
    parser.add_argument('-s','--specify', type=str, default='',help='收集指定目录或者指定文件，通常用于添加配置文件到压缩包。使用该参数时，log-types必须包含"specify"的日志类型。') 
    parser.add_argument('-f','--sftp-server', type=str, default='',help='默认生成在当前用户桌面，不上传日志；如需上传日志，请设置有效sftp服务器地址，通常设置为UCSS IP，也使用其他sftp服务器。')
    parser.add_argument('-o','--sftp-port', type=int, default=22,help='sftp 服务器端口号。') 
    parser.add_argument('-u','--sftp-username', type=str, default='skyguardts',help='sftp服务器用户名，默认使用skyguardts用户名。') 
    parser.add_argument('-p','--sftp-password', type=str, default='',help='sftp服务器密码，如果使用UCSS当作服务器，请连续天空卫士技术团队获取技术支持密码。') 
    parser.add_argument('-k','--sftp-key-file', type=str, default='',help='sftp服务器的private key') 
    parser.add_argument('-e','--sftp-server-dest-dir', type=str, default='/tmp/',help='sftp 服务器上传的目标目录。')
    args = parser.parse_args()
    version = args.version
    log_type = args.log_types
    sdk_debug = args.debug.upper()
    wait_seconds = args.time
    specify = args.specify
    sftp_server = args.sftp_server
    sftp_port = args.sftp_port
    sftp_username = args.sftp_username
    sftp_password = args.sftp_password
    sftp_key_file = args.sftp_key_file
    sftp_dest_dir = args.sftp_server_dest_dir
    """
    #print '\n'
    print('---------------------Start 使用示例--------------------------------')
    print('1. 获取更多参数帮助：python WepLogs.py -h') 
    print('2. 默认不加任何参数时，仅收集agent和adk的日志，日志基本默认为INFO：python WepLogs.py')
    print('3. 加参数时，使用示例： python WepLogs.py -v v2.3.0 -l agent,sdk,hook,specify -d DEBUG -t 300 -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc\"')
    print('4. 可以开启DEBUG模式后300秒，再[agent, sdk]收集日志： python WepLogs.py -d DEBUG -t 300 ')
    print('\n')
    """
    desciption =  '终端版本：%s ，收集的日志包括：%s ，UCSC 日志level模式：%s , 等待时间：%s秒, 指定目录: %s。' % (version,log_type,sdk_debug,wait_seconds,specify)
    addition = ''
    log_type = log_type.split(',')
    if sdk_debug in ['DEBUG','TRACE']:
        if wait_seconds>0:
            addition = '\n 开启或切换日志模式为%s，并延迟%s 秒收集日志。'% (sdk_debug,wait_seconds)
        else:
            addition = '\n 仅仅开启或切换日志模式为%s，不收集日志。'% sdk_debug
        #sdk_debug = True
    else:
        sdk_debug = 'INFO'
    if specify:
        addition = addition + '收集的指定目录或者文件： %s'% specify
    desciption = desciption + addition
    #print('---------------------End 使用示例 --------------------------------\n')
    print('---------------------收集 DLP 日志：--------------------------------')
    print('当前参数设置如下：')
    print(desciption)
    wep_log_obj = WepLogCollection(ep_version=version,types=log_type,specify=specify,debug=sdk_debug,timer=wait_seconds)
    print('wep_log_obj.output_logs=',wep_log_obj.output_logs)
    if wep_log_obj.output_logs:
        print('完成终端日志收集，日志输出目录为：\n%s' % wep_log_obj.output_logs)
        if sftp_server:
            print('---------------------正在上传已收集的DLP日志--------------------------------')
            sftp = SftpClient(ip=sftp_server,port=sftp_port,username=sftp_username,password=sftp_password,private_key_file=sftp_key_file)
            dest_server_file = os.path.join(sftp_dest_dir, wep_log_obj.output_logs.split('\\')[-1])
            sftp.put(wep_log_obj.output_logs, dest_server_file)
            print('完成日志上传，至目标服务器%s： %s' % (sftp_server,dest_server_file))
        else:
            pass
    else:
        pass
    #wep_log_obj.tar_dlp_log_files()
    #wep_log_obj.set_sdklog_level(level='INFO')
    