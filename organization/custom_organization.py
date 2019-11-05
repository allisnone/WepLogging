# -*- coding: utf-8 -*-
#Author zhangguoxin
def read_file(file='custom_user0.csv',encoding='utf-8-sig',type='r'):
    """
    说明：如使用utf-8编码，文件的起始会出现：'\ufeff’ 字符，故使用utf-8-sig编码
    :param file: str
    :param encoding: str
    :param type: str
    :return: list, 按行读取文件的数据列表，每一行最后字符为\n
    """
    lines = []
    try:
        txtfile = open(file, type, encoding=encoding)
        lines = txtfile.readlines()
    except Exception as e:
        print('ERROR-读取文件{0}错误: {1}'.format(file,e))
    return lines

def get_standard_template_colums(file='custom_user0.csv',encoding='utf-8-sig'):
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
        return [],[],False
    else:
        if len(datas)==1:
            print('ERROR: 读取的文件%s仅有文件头' % csv_file)
            return [],[],False
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

def check_custom_user(datas, standard_columns,uniq_index=[0,1,2,3,9],department_uuids=[],depend_department_check=False):
    """
    天空卫士自定义组织机构，检查custom_user.csv 文件的有效性
    :param datas: str, line data for custom_user or custom_computer
    :param standard_columns: list, standard columns for reference: custom_user or custom_computer
    :param uniq_index: list, the column should be unique
    :param department_uuids: list, valid department uuid list
    :param end_department_check, bool , default False
    :return: list, 有错误的用户数据
    """
    columns_count = len(standard_columns)
    error_lines = []
    #uniq_index = [0,1,2,3,9]
    uniq_count = len(uniq_index)
    uniq_list = []
    for g in range(0,uniq_count):
        h = []
        if not department_uuids and g==0:
            h = ['0','1']
        uniq_list.append(h)
    #print(uniq_list)
    #print('len(datas)')
    for i in range(1,len(datas)):
        if i>5:
            pass
            #break
        raw_user_datas = datas[i]
        #print('uniq_list',uniq_list)
        user_list = raw_user_datas.replace('\n','').split(',')
        #print('user_list=',user_list)
        #检查每个用户的字段数是否足够
        this_len = len(user_list)
        if depend_department_check:
            depend_department_id = user_list[-1]
            #print('depend_department_id=',depend_department_id)
            #print(uniq_list[0])
            if depend_department_id in uniq_list[0]:
                pass
            else:
                print('ERROR-department上级部门ID=%s未定义，第%s行 ，用户数据: %s' % (depend_department_id, i+1, raw_user_datas))
        if this_len==columns_count:
            if this_len==11 and user_list[0]==user_list[7]:
                print('ERROR-主管不能是自己ID=%s，第%s行 ，用户数据: %s' % (user_list[0], i+1, raw_user_datas))
            #检查用户ID和主管ID是否一样，主管不能是自己
            pass
        else:
            print('ERROR-字段数不匹配-总共%s个字段，要求%s个字段： 第%s行，用户数据: %s' % (this_len,columns_count,i+1, raw_user_datas))
            error_lines.append(user_list)
        #检查非空字段是否为空和唯一性字段是否唯一
        for k in range(0,uniq_count):
            j = uniq_index[k]
            value = user_list[j]
            #print('i=%s k=%s j= %s value=%s'%(i,k,j,value))
            #print(uniq_list[k])
            #print('uniq_list[{0}]={1}'.format(k,uniq_list[k]))
            #print('kkkk')
            if value:
                #print('department_uuids=',department_uuids)
                temp_empty = value.replace(' ','').replace('    ','')
                if not temp_empty:#替换空格或者tab健后为空字符
                    print('ERROR-非空字段为空，第%s行，第%s字段%s为 空字符，用户数据：%s' % (i+1, j+1 , standard_columns[j], raw_user_datas))
                    error_lines.append(user_list)
                if department_uuids:#用户检查
                    if value in uniq_list[k] and standard_columns[j]!='department':
                        print('ERROR-custom_user唯一性字段不唯一，第%s行 ，重复字段 %s=%s， 用户数据: %s' %(i+1, standard_columns[j], value, raw_user_datas))
                    else:
                        uniq_list[k].append(value)
                else:#部门检查
                    if value in uniq_list[k]:
                        print('ERROR-department唯一性字段不唯一，第%s行 ，重复字段 %s=%s， 用户数据: %s' % (i+1, standard_columns[j], value, raw_user_datas))
                    else:
                        #print('k=',k)
                        uniq_list[k].append(value)
                        #print('k=',k,'value=',value)
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
        if i>len(datas)-3:
            #print('aaa')
            #print(uniq_list)
            pass
            #break
    #print('uniq_list=',uniq_list[0])        
    return uniq_list,error_lines
    