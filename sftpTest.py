# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-01-26
import argparse
import importlib
import sys
import tarfile
import time
import os
import shutil
import paramiko
#https://www.linuxhub.org/?p=2631
def upload_dlp_logs2_ucss(user='skyguardts',passwd='473385fc'):
    ucss_ip = '172.22.80.205'
    ucss_ssh_port = 12039
    log_file_name = r'C:\Users\\zhangguoxin\Desktop\skyguard_wep_201902021206.tar.gz' 
    #private_key = paramiko.RSAKey.from_private_key_file('id_rsa31')
    transport = paramiko.Transport((ucss_ip, ucss_ssh_port))
    transport.connect(username=user, password=passwd)
    #transport.connect(username="skyguardts", pkey=private_key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(log_file_name, '/tmp/skyguard_wep_201902021206.tar.gz')
    #sftp.get('/filedir/oldtext.txt', r'C:\Users\duany_000\Desktop\oldtext.txt')
    transport.close()
upload_dlp_logs2_ucss()