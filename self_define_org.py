# -*- coding: utf-8 -*-
def read_file(file='custom_user0.csv',encoding='utf-8',type='r'):
    """
    :param file: str
    :param encoding: str
    :param type: str
    :return: list, 按行读取文件的数据列表，每一行最后字符为\n
    """
    txtfile = open(file, type, encoding=encoding)
    lines = txtfile.readlines()
    return lines

def get_standard_template_colums(file='custom_user0.csv',encoding='utf-8'):
    #['\ufeffuuid', 'commonName', 'mail', 'logonName', 'ip', 'enableManager', 'title', 'manager', 'telephone', 'department', 'departmentName\n']
    """
    :param file: str
    :param encoding: str
    :return: list, 返回文件第一行，文件头
    """
    datas = read_file(file, encoding)
    if datas:
        return datas[0].replace('\n','').split(',')
    else:
        return []
    
def check_csv_head(csv_file,standard_csv_file='custom_user0.csv',standard_columns=[]):
    """
    天空卫士自定义组织机构，检查csv 文件头的有效性
    :param csv_file: str, department/custom_user/computer csv file
    :param standard_columns: list, standard custom_user columns
    :return: list, 有错误的用户数据
    """
    if not standard_columns:
        standard_columns = get_standard_template_colums(file=standard_csv_file)
    datas = read_file(csv_file)
    if not datas:
        print('ERROR: 读取的文件%s无数据' % csv_file)
        return []
    else:
        if len(datas)==1:
            print('ERROR: 读取的文件%s仅有文件头' % csv_file)
            return []
        else:
            pass
    columns = datas[0].replace('\n','').split(',')
    different_columns = list(set(standard_columns).difference(set(columns)))
    if different_columns:
        print('ERROR-缺少文件头字段： %s 比标准模板少几列：%s'% (csv_file, different_columns))
    different_columns1 = list(set(columns).difference(set(standard_columns)))
    if different_columns1:
        print('ERROR-多余文件头字段：%s 比标准模板多几列：%s' % (csv_file, different_columns1))
    if not different_columns and not different_columns1:
        return datas,standard_columns,True
    else:
        return datas,standard_columns,False

def check_custom_user(datas, standard_columns,uniq_index=[0,1,2,3,9],department_uuids=[]):
    """
    天空卫士自定义组织机构，检查custom_user.csv 文件的有效性
    :param csv_file: str, custom_user csv file
    :param standard_columns: list, standard custom_user columns
    :param department_uuids: list, valid department uuid list
    :return: list, 有错误的用户数据
    """
    columns_count = len(standard_columns)
    error_lines = []
    #uniq_index = [0,1,2,3,9]
    uniq_count = len(uniq_index)
    uniq_list = [[]]*uniq_count
    if not department_uuids:
        uniq_list = [['1']]*uniq_count
    for i in range(1,len(datas)):
        raw_user_datas = datas[i]
        user_list = raw_user_datas.replace('\n','').split(',')
        print('user_list=',user_list)
        #检查每个用户的字段数是否足够
        if len(user_list)==columns_count:
            pass
        else:
            print('ERROR-字段数不匹配： 第%s行，用户数据: %s' % (i, raw_user_datas))
            error_lines.append(user_list)
        #检查非空字段是否为空和唯一性字段是否唯一
        if i>235:
            #pass
            break
        for k in range(0,uniq_count):
            j = uniq_index[k]
            value = user_list[j]
            print('i=%s k=%s j= %s value=%s'%(i,k,j,value))
            print('uniq_list[{0}]={1}'.format(k,uniq_list[k]))
            if value:
                print('department_uuids=',department_uuids)
                if department_uuids:#用户检查
                    if value in uniq_list[k] and standard_columns[j]!='department':
                        print('ERROR-custom_user唯一性字段不唯一，第%s行 ，重复字段 %s=%s， 用户数据: %s' %(i+1, standard_columns[j], value, raw_user_datas))
                    else:
                        uniq_list[k].append(value)
                else:#部门检查
                    if value in uniq_list[k]:
                        print('ERROR-department唯一性字段不唯一，第%s行 ，重复字段 %s=%s， 用户数据: %s' %(i+1, standard_columns[j], value, raw_user_datas))
                    else:
                        uniq_list[k].append(value)
            else:
                print('ERROR-非空字段为空，第%s行，第%s字段%s为 空字符，用户数据：%s' % (i+1, j+1 , standard_columns[j], raw_user_datas))
                error_lines.append(user_list)
            #检查uuid是否重复
            if j==0: #uuid
                if department_uuids and value in department_uuids:
                    print('ERROR-部门和用户uuid重复混淆，第%s行 ，uuid=%s， 用户数据: %s' %(i+1, value, raw_user_datas))
                else:
                    pass
            elif j==9: #部门uuid是否存在,且有效
                if department_uuids and value in department_uuids:
                    pass
                else:
                   print('ERROR-用户部门不存在，第%s行 ，用户部门：%s， 用户数据: %s' %(i+1, value, raw_user_datas))
            else:
                pass
            
    return uniq_list,error_lines

def get_department_uuid(csv_file, standard_columns):
    """
    天空卫士自定义组织机构，检查department.csv 文件的有效性
    :param csv_file: str, custom_user csv file
    :param standard_columns: list, standard custom_user columns
    :param department_uuids: list, valid department uuid list
    :return: list, 有错误的用户数据
    """
    datas,is_healthy_header = check_csv_head(csv_file, standard_columns)
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
                print('ERROR-上级部门必须先定义: 第%s行部门的parent_department_id=%s未定义，部门信息: %s' % (i+1, parent_department_id,department_datas[i]))
            #uuid 重复性检查
            if uuid not in department_uuids:
                department_uuids.append(uuid)
            else:
                print('第%s行部门的uuid重复，重复的uuid: %s, 部门信息: %s' % (i+1, uuid,department_datas[i]))
    return department_uuids


custom_user_csv = 'custom_user.csv'
standard_custom_user_csv ='custom_user0.csv'
department_csv = 'department.csv'
standard_department_csv = 'department0.csv'
department_datas,department_standard_columns,is_healthy_department_headers = check_csv_head(department_csv,standard_csv_file=standard_department_csv)
print('department_datas=',department_datas)
department_uniq_list,error_department_lines = check_custom_user(department_datas, department_standard_columns,uniq_index=[0,1])
department_uuids = department_uniq_list[0]
print('department_uuids=',department_uniq_list)
user_datas,user_standard_columns,is_healthy_user_headers = check_csv_head(custom_user_csv,standard_csv_file=standard_custom_user_csv)

#user_uniq_list,error_user_lines = check_custom_user(user_datas, user_standard_columns,uniq_index=[0,1,2,3,9],department_uuids=department_uuids)
