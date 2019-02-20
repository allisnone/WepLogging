# -*- coding: utf-8 -*-
def read_file(file='custom_user0.csv',encoding='utf-8'):
    txtfile = open(file, 'r', encoding='utf-8')
    lines = txtfile.readlines()
    return lines

def get_standard_template_file(csv='custom_user0.csv'):
    #['\ufeffuuid', 'commonName', 'mail', 'logonName', 'ip', 'enableManager', 'title', 'manager', 'telephone', 'department', 'departmentName\n']
    txtfile = open(csv, 'r', encoding='utf-8')
    users = txtfile.readlines()
    columns = users[0].split(',')
    return  columns

def check_file(from_file='custom_user.csv', standard_columns=[],department_uuids=[]):
    """
    用于url分类测试，测试文件中存放大量的url地址
    :param from_file: str 
    :return: list， users（Generator）
    """
    txtfile = open(from_file, 'r',encoding='utf-8')
    users = txtfile.readlines()
    columns = users[0].split(',')
    different_columns = list(set(standard_columns).difference(set(columns)))
    if different_columns:
        print('%s 比标准模板少了以下几列：%s'% (from_file, different_columns))
    different_columns1 = list(set(columns).difference(set(standard_columns)))
    if different_columns1:
        print('%s 比标准模板多了以下几列：%s' % (from_file, different_columns1))
    columns_count = len(columns)
    error_lines = []
    V23_NON_NUM_INDEX_USER = [0,1,2,3,9]
    uniq_count = len(V23_NON_NUM_INDEX_USER)
    uniq_list = [[]]*uniq_count
    for i in range(1,len(users)):
        user_list = users[i].split(',')
        #检查是否确实字段
        
        if len(user_list)==columns_count:
            pass
        else:
            print('ERROR user i=%s user_list: %s' % (i, user_list[i]))
            error_lines.append(user_list)
        #检查非空字段
        k = 0
        for k in range(0,uniq_count):
            j = V23_NON_NUM_INDEX_USER[k]
            value = user_list[j]
            if value:
                if value in uniq_list[k] and standard_columns[j]!='department':
                    print('%s 字段中 %s 重复' %(standard_columns[j], value))
                else:
                    uniq_list[k].append(value)
                pass
            else:
                print('ERROR 非空字段检查出错，行号i=%s 第%s个字段%s为空，该行内容%s' % (i+1, j , stand_c[j], user_list))
                error_lines.append(user_list)
            if j==0: #uuid
                if value in department_uuids:
                    print('user_uuid 和 department_uuid重复')
                else:
                    pass
            elif j==9: #部门uuid是否存在
                if value in department_uuids:
                    pass
                else:
                   print('用户的 department_uuid不存在') 
            else:
                pass
            
    return error_lines

def get_department_uuid():
    department_datas = read_file(file='department.csv')
    department_uuids = ['1']
    for i in range(1,len(department_datas)):
        department_data = department_datas[i].split(',')
        if department_data:
            uuid = department_data[0]
            parent_department_id = department_data[-1].replace('\n','')
            #parent uuid必须先定义检测
            if parent_department_id in department_uuids:
                pass
            else:
                print('ERROR 上级部门必须先定义: 第%s行部门的parent_department_id=%s未定义，部门信息: %s' % (i+1, parent_department_id,department_datas[i]))
            #uuid 重复性检查
            if uuid not in department_uuids:
                department_uuids.append(uuid)
            else:
                print('第%s行部门的uuid重复，重复的uuid: %s, 部门信息: %s' % (i+1, uuid,department_datas[i]))
    return department_uuids

V23_NON_NUM_INDEX_USER = [0,1,2,3,9]
stand_c = get_standard_template_file(csv='custom_user0.csv')
print('stand_c=',stand_c)
from_file='custom_user.csv'


department_uuids = get_department_uuid()
check_file(from_file,stand_c,department_uuids)