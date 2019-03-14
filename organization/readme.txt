使用方法
1、安装python3环境
2、直接替换custom_user.csv和department.csv文件后，直接运行.py文件即可
python -d <department csv文件> -u <custom_user csv 文件> -p <computer csv文件>
默认情况：department.csv，custom_user.csv，computer.csv 放在.py文件同一目录直接运行直可：
 python customOrganization.py   
 
也可以把检查结果导出为文件 查看：
python customOrganization.py  > result.txt

3、todo