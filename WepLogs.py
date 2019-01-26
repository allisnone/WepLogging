# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-01-26
import argparse
import datetime
import tarfile
import os

class WepLogCollection:
    """
    用于收集终端的日志
    """
    def __init__(self, ep_version='v2.3.0',types='',out_put_dir=''):
        self.ep_version = ep_version
        self.log_types = types
        self.out_put_dir = out_put_dir
        self.agent_log_dir = ''
        self.ucsc_sdk_log_dir = ''
        self.app_hook_dir = ''
        self.install_log = ''
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
                print 'ERROR-输入无效的日志类型：%s' % types
        elif isinstance(types, list): #给定多种类型，list 
            invalid_log_types = list(set(types).difference(set(valid_log_types)))
            if invalid_log_types:
                print 'ERROR-输入无效的多种日志类型：%s' % invalid_log_types
            #如果有无效的日志类型，剔除无效的日志类型
            self.log_types = list(set(valid_log_types).intersection(set(types)))
        else:
            print 'ERROR-输入其他无效的日志类型：%s，请确保数日str或者是list类型！' % type(types)
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
            print 'log_dir_data=',log_dir_data
            if version:
                log_dir_data = self.all_version_datas[self.ep_version]
            all_this_version_types = log_dir_data.keys()
            print 'all_this_version_types=',all_this_version_types
            
            if self.log_types=='default':
                self.log_types = ['agent','sdk']
            elif self.log_types=='all':
                self.log_types = log_dir_data
            else:
                pass
            print self.log_types
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
            print 'ERROR：请设置正确的ep_version或更新all_version_datas！'
            return {} 
        
    def tar_file(self):
        log_dir_data = self.get_version_data()
        if log_dir_data:
            date_str = '20190126'
            print os.environ 
            print os.getenv('APPDATA')
            print os.getenv('PROGRAMW6432')
            print os.getenv('TEMP')
            print os.getenv('USERPROFILE')
            desktop_dir = os.path.join(os.path.expanduser("~"), 'Desktop')
            tar_file_name = 'skyguard_wep_'  + date_str + '.tar.gz'
            full_tar_file_name = os.path.join(desktop_dir,tar_file_name)
            print 'full_tar_file_name=',full_tar_file_name
            tar_obj = tarfile.open(full_tar_file_name,'w:gz')
            #获取字典中非空的数据
            log_dir_data = {k: v for k, v in log_dir_data.iteritems() if v}
            log_dirs = [v for k, v in log_dir_data.iteritems() if v]
            #print log_dir_data
            #print log_dirs
            profix_dirs = ['PROGRAMW6432_','APPDATA_','TEMP_']
            for dir in log_dirs:
                print dir
                for profix in profix_dirs:
                    if profix in dir:
                        dirs = dir.split('_')
                        print 'dirs=',dirs
                        this_dir = os.path.join(os.getenv(dirs[0]),dirs[1])
                        print 'this_dir=',this_dir
                        if this_dir and os.path.exists(this_dir):
                            tar_obj.add(this_dir) 
                else:
                    pass
            tar_obj.close()
            print '完成终端日志收集，日志输出目录为：%s' % full_tar_file_name
        else:
            pass
        return
    
    def enable_sdk_debug(self,level='DEBUG'):
        sdk_util = os.path.join(os.getenv('PROGRAMW6432'),'SkyGuard\\SkyGuard Endpoint\\UCSCSDK\\bin\\ucsc_util.exe')
        return
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script') 
    parser.add_argument('--version', type=str, default = 'v2.3.0') 
    parser.add_argument('--log-type', type=str, default= 'default')
    parser.add_argument('--sdk-debug', type=str, default='disable')
    parser.add_argument('--wait-seconds', type=int, default=300) 
    parser.add_argument('--specify', type=str, default='') 
    args = parser.parse_args()
    version = args.version
    log_type = args.log_type
    sdk_debug = args.sdk_debug
    wait_seconds = args.wait_seconds
    specify = args.specify
    print '\n'
    print '---------------------Start 使用说明 --------------------------------'
    print '1. 直接使用：python main.py' 
    print '2. 默认不加任何参数时，相当于（不做日期过滤）：python main.py --unit-size=10G --forensics=network'
    print '3. 加参数时，使用示例： python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115'
    print '4. 也可以使用重定向输出日志到文件，比如： '
    print '   python main.py --unit-size=5G --forensics=network --start-date=20181101 --end-date=20190115 > output_log.txt'
    print '5. 如果仅仅预演压缩的结果而不进行实质性压缩，使用以下替换命令后，再运行程序，如：'
    print "   sed -i 's/tar.add/#tar.add/g' bundle_tarfile.py"
    print '\n'
    print '当前参数设置如下：'
    desciption =  '终端版本：%s ，收集的日志包括：%s ，UCSC DEBUG模式：%s 。' % (version,log_type,sdk_debug)
    addition = ''
    if sdk_debug=='enable':
        addition = '\n 开启debug模式后延迟%s 秒收集日志。'% wait_seconds
    if specify:
        addition = addition + '收集的指定目录或者文件： %s'% specify
    desciption = desciption + addition
    print desciption
    print '---------------------End 使用说明 --------------------------------\n'
    wep_log_obj = WepLogCollection(ep_version=version,types=log_type,out_put_dir='')
    wep_log_obj.tar_file()
    