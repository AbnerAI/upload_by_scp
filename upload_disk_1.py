import os
import fnmatch
import sys

# 指定要搜索的根目录
root_path = "G:/qsiPrepadd/"
# 目标文件的可能后缀
suffixes = [
    "_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
    "_space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz"
]

import paramiko
import os
from scp import SCPClient

# 设置服务器的连接信息
host = "172.16.185.196"
port = 22  # 默认SSH端口
username = "root"
password = "jhHfs##r=t1bhuL"  # 或者使用SSH密钥进行认证

# 创建SSH客户端实例
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接到服务器
ssh_client.connect(host, port, username, password)

# 创建SCP客户端实例
scp_client = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
sftp = ssh_client.open_sftp()

def recursive_makedirs(sftp, path):
    try:
        sftp.mkdir(path)
    except IOError:
        # 递归创建所有父目录
        recursive_makedirs(sftp, os.path.dirname(path))
        sftp.mkdir(path)

# ...



# 存储找到的文件对
found_files = []
ind = 0
# 快速遍历目录树，寻找包含 "anat" 的路径
for dirpath, dirnames, _ in os.walk(root_path):
    if "anat" in dirnames:
        # 构造 "anat" 目录的路径
        anat_path = os.path.join(dirpath, "anat")
        # 预设一个空字典，用于匹配文件名中共有的部分
        file_matches = {}
        # 检查目标文件是否存在于 "anat" 目录下
        for entry in os.listdir(anat_path):
            for suffix in suffixes:
                if entry.endswith(suffix):
                    # 提取文件名中除后缀外的部分作为键
                    key = entry[:-len(suffix)]
                    if key not in file_matches:
                        file_matches[key] = [None, None]
                    # 标记找到的文件类型
                    if "T1w" in suffix:
                        file_matches[key][0] = entry
                    else:
                        file_matches[key][1] = entry
        # 检查并收集匹配的文件对
        for key, files in file_matches.items():
            if all(files):  # 确保两种类型的文件都找到了
                print(ind)
                ind += 1
                print((os.path.join(anat_path, files[0]), os.path.join(anat_path, files[1])))
                found_files.append((os.path.join(anat_path, files[0]), os.path.join(anat_path, files[1])))

                # 定义本地目录和远程目录
                # local_path = "E:/T7/test"
                remote_path = "/mnt/data3/ABCD_2024_0326/"
                local_path = anat_path
                remote_path =  os.path.join(remote_path, os.path.dirname(local_path).replace("G:/", "").replace("\\","/"))

                # # sftp.mkdir(remote_path)
                # print(remote_path)
                # exit(0)
                # 使用递归函数创建目录
                try:
                    status_info = sftp.stat(remote_path)
                    print('skip')
                except:
                    recursive_makedirs(sftp, remote_path)
                    scp_client.put(local_path, remote_path, recursive=True)

# 关闭连接
scp_client.close()
ssh_client.close()
