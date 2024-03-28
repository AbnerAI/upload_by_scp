import paramiko
import os
from scp import SCPClient

# 指定要搜索的根目录
root_path = "G:/ABCD/"

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

# 存储找到的文件对
found_files = []
ind = 0
# 快速遍历目录树，寻找包含 "anat" 的路径
for dirpath, dirnames, _ in os.walk(root_path):
    if "anat" in dirnames:
        # 构造 "anat" 目录的路径
        anat_path = os.path.join(dirpath, "anat")
        print(anat_path)
        print(ind)
        ind += 1

        # 定义本地目录和远程目录
        # local_path = "E:/T7/test"
        remote_path = "/mnt/data3/ABCD_2024_0326/"
        local_path = anat_path
        remote_path =  os.path.join(remote_path, os.path.dirname(local_path).replace("G:/", "").replace("\\","/"))

        try:
            status_info = sftp.stat(remote_path)
            print('skip')
        except:
            recursive_makedirs(sftp, remote_path)
            scp_client.put(local_path, remote_path, recursive=True)

# 关闭连接
scp_client.close()
ssh_client.close()
