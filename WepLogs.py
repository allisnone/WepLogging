# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-01-26
import argparse
import datetime
import tarfile
import time
import os

class WepLogCollection:
    """
    用于收集终端的日志
    """
    def __init__(self, ep_version='v2.3.0',types='',out_put_dir='',debug=False,timer=300):
        self.ep_version = ep_version
        self.log_types = types
        self.out_put_dir = out_put_dir
        self.sdk_debug = debug
        self.timer = timer
        self.specify_files = ''
        self.valid_versions = ['v2.3.0', 'v2.2.0']
        self.log_dir_data = {}
        
    def initial_datas(self):
        self.set_all_version_datas()    
        
    def get_agent_version(self): 
        return       
    
    def set_valid_agent_versions(self,versions=[]):
        self.valid_versions = versions
        return
    
    def set_agent_version(self,version='v2.3.0'):
        self.ep_version = version.lower()
        return
    
    def is_valid_ep_version(self,version=''):
        if version: 
            return version.lower() in list(self.all_version_datas.keys())
        return self.ep_version in list(self.all_version_datas.keys())
    
    def set_log_types(self,types='',specify=''):
        """
        设置要收集的日志类型，如果需要收集特殊日志或者配置文件，参数specify必须非空
        :parama types: str or list type
        """
        valid_log_types = ['agent','sdk','hook','install','specify']
        if types:
            pass
        else:#默认只取agent和sdk的日志
            #types = 'default'
            if not self.log_types:
                self.log_types = ['agent','sdk']
        if isinstance(types,str): #一种类型
            if types in valid_log_types:
                self.log_types = [type]
                if types=='default': #默认只取agent和sdk的日志
                    self.log_types = ['agent','sdk']
                else:
                    pass
            elif types=='default': #默认只取agent和sdk的日志
                    self.log_types = ['agent','sdk']
            elif types=='all': #收取全部日志
                    self.log_types = valid_log_types
            else:
                print('ERROR：输入无效的日志类型：%s' % types)
        elif isinstance(types, list): #给定多种类型，list 
            invalid_log_types = list(set(types).difference(set(valid_log_types)))
            if invalid_log_types:
                print('ERROR-输入无效的多种日志类型：%s' % invalid_log_types)
            #如果有无效的日志类型，剔除无效的日志类型
            self.log_types = list(set(valid_log_types).intersection(set(types)))
        else:
            print('ERROR-输入其他无效的日志类型：%s，请确保数日str或者是list类型！' % type(types))
        if specify and 'specify' in self.log_types: #设置特殊目录日志
            self.specify = specify
        return
    
    def set_all_version_datas(self,datas={}):
        self.all_version_datas = {
            'v2.3.0':{
                'agent': 'PROGRAMW6432_SkyGuard\SkyGuard Endpoint\EndpointAgent\\var\\log\\',
                'sdk': 'PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\log\\',
                'hook': 'APPDATA_SkyGuard\SkyGuard Endpoint\\var\\log\\',
                'install': 'TEMP_EndpointInstaller.log',
                'sdkdb': '%PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\cache\\',
                'specify': ''
                },
            'v2.2.0':{
                'agent': 'PROGRAMW6432_SkyGuard\SkyGuard Endpoint\EndpointAgent\\var\\log\\',
                'sdk': 'PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\log\\',
                'hook': 'APPDATA_SkyGuard\SkyGuard Endpoint\\var\\log\\',
                'install': 'TEMP_EndpointInstaller.log',
                'sdkdb': '%PROGRAMW6432_SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\var\\cache\\',
                'specify': ''
                },   
            }
        if datas:
            self.all_version_datas = datas
        return
            
    def get_version_data(self,version=''):
        self.set_all_version_datas()  
        if self.is_valid_ep_version(version):
            log_dir_data = self.all_version_datas[self.ep_version]
            #print 'log_dir_data=',log_dir_data
            if version:
                log_dir_data = self.all_version_datas[self.ep_version]
            all_this_version_types = list(log_dir_data.keys())
            #print 'all_this_version_types=',all_this_version_types
            
            if self.log_types=='default':
                self.log_types = ['agent','sdk']
            elif self.log_types=='all':
                self.log_types = log_dir_data
            else:
                pass
            #print self.log_types
            #print log_dir_data[self.log_types]
            except_logs_types = list(set(all_this_version_types).difference(self.log_types))
            if except_logs_types: #收集已定义日志类型中的一部分
                for type in except_logs_types:
                    log_dir_data[type] = ''
                    #if type=='specify' and self.specify:
                    #    log_dir_data['specify'] = self.specify
            else:#全部收集
                pass
            if 'specify' in self.log_types and self.specify:
                log_dir_data['specify'] = self.specify
            else:
                pass
            return log_dir_data
        else:
            print('ERROR：请设置正确的ep_version或更新all_version_datas！')
            return {} 
        
    def tar_dlp_log_files(self):
        """
        根据参数设置sdk 日志level，并收集日志，打包压缩
        :return: 打包压缩的文件名
        """
        full_tar_dlp_log_files_name = ''
        log_dir_data = self.get_version_data()
        if self.sdk_debug in ['DEBUG', 'TRACE']:
            #DEBUG或者TRACE模式时，设置SDK 的log level
            self.set_sdklog_level()
            if self.timer>0: #DEBUG或者Trace模式，同时时间大于0时，等待若干秒
                print('已开启SDK日志模式: %s, 将等待%s秒后自动收集日志...' % (level,self.timer))
                time.sleep(self.timer)
            elif self.timer==0:  #仅开启DEBUG或者TRACE模式，且不收集日志
                print('仅开启SDK日志模式: %s' % level)
                return
            else:#无效时间
                return
        if log_dir_data:
            date_str = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
            #print os.environ 
            #print os.getenv('APPDATA')
            #print os.getenv('PROGRAMW6432')
            #print os.getenv('TEMP')
            #print os.getenv('USERPROFILE')
            desktop_dir = os.path.join(os.path.expanduser("~"), 'Desktop')
            tar_dlp_log_files_name = 'skyguard_wep_'  + date_str + '.tar.gz'
            full_tar_dlp_log_files_name = os.path.join(desktop_dir,tar_dlp_log_files_name)
            #print 'full_tar_dlp_log_files_name=',full_tar_dlp_log_files_name
            tar_obj = tarfile.open(full_tar_dlp_log_files_name,'w:gz')
            #获取字典中非空的数据
            log_dir_data = {k: v for k, v in log_dir_data.items() if v}
            log_dirs = [v for k, v in log_dir_data.items() if v]
            #print log_dir_data
            #print log_dirs
            profix_dirs = ['PROGRAMW6432_','APPDATA_','TEMP_']
            for dir in log_dirs:
                #print dir
                for profix in profix_dirs:
                    if profix in dir:
                        dirs = dir.split('_')
                        #print 'dirs=',dirs
                        this_dir = os.path.join(os.getenv(dirs[0]),dirs[1])
                        #print 'this_dir=',this_dir
                        if this_dir and os.path.exists(this_dir):
                            tar_obj.add(this_dir) 
                else:
                    pass
            tar_obj.close()
            print('完成终端日志收集，日志输出目录为：%s' % full_tar_dlp_log_files_name)
        self.restore_log_level()
        return full_tar_dlp_log_files_name
    
    def set_sdklog_level(self,level=''):
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
            print('ERROR: 文件不存在%s' % sdk_util)
        return is_swtich_successful
    
    def restore_log_level(self):
        if self.sdk_debug in ['DEBUG', 'TRACE']:
            self.set_sdklog_level(level='INFO')
        return
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script') 
    parser.add_argument('-v','--version', type=str, default = 'v2.3.0',help='指定需收集日志的终端的版本，格式如v2.3.0') 
    parser.add_argument('-l','--log-types', type=str, default= 'default',help='收集终端模块的日志类型，有效类型：all（除specify以外的所有类型）, defualt（agent,sdk两种）, 或[agent,sdk,hook,install,specify]的任意组合-需以英文逗号分隔。')
    parser.add_argument('-d','--debug', type=str, default='INFO',help='是否开启或者切换SDK日志level，有效level为: INFO, DEBUG, TRACE；其他输入为无效，不改变sdk的日志模式。')
    parser.add_argument('-t','--time', type=int, default=300,help='先切换SDK的日志模式，等待若干秒后，再收集日志，与-d DEBUG（或TRACE）参数组合使用；通常用于收集特定场景的日志。') 
    parser.add_argument('-s','--specify', type=str, default='',help='收集指定目录或者指定文件，通常用于添加配置文件到压缩包。使用该参数时，log-types必须包含"specify"的日志类型') 
    args = parser.parse_args()
    version = args.version
    log_type = args.log_types.split(',')
    sdk_debug = args.debug.upper()
    wait_seconds = args.time
    specify = args.specify
    #print '\n'
    print('---------------------Start 使用示例--------------------------------')
    print('1. 获取更多参数帮助：python WepLogs.py -h') 
    print('2. 默认不加任何参数时，仅收集agent和adk的日志，日志基本默认为INFO：python WepLogs.py')
    print('3. 加参数时，使用示例： python WepLogs.py -v v2.3.0 -l agent,sdk,hook,specify -d DEBUG -t 300 -s "C:\Program Files\SkyGuard\SkyGuard Endpoint\EndpointAgent\etc\"')
    print('4. 可以开启DEBUG模式后300秒，再[agent, sdk]收集日志： python WepLogs.py -d DEBUG -t 300 ')
    print('\n')
    print('当前参数设置如下：')
    desciption =  '终端版本：%s ，收集的日志包括：%s ，UCSC 日志level模式：%s 。' % (version,log_type,sdk_debug)
    addition = ''
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
    print(desciption)
    print('---------------------End 使用示例 --------------------------------\n')
    wep_log_obj = WepLogCollection(ep_version=version,types=log_type,out_put_dir='',debug=sdk_debug,timer=wait_seconds)
    wep_log_obj.tar_dlp_log_files()
    #wep_log_obj.set_sdklog_level(level='INFO')
    