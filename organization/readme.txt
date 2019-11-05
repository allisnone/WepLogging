使用方法
1、安装python3环境；如使用python2环境，需另行修改代码，自行替换“print”方法
2、直接替换data目录下 custom_user.csv、computer.csv 和department.csv文件后，直接运行.py文件即可

默认情况，读取data目录下的：department.csv，custom_user.csv，computer.csv ，把要坚持的文件放该目录后直接运行：
python customOrganization.py   
 
也可以把检查结果导出为文件 查看：
python customOrganization.py  > result.txt

如需指定查文件的路径：
python -d <department csv文件> -u <custom_user csv 文件> -p <computer csv文件>   > result.txt

注：必须不能删除stardard目录及文件
3、todo