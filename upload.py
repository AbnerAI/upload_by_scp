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

# 定义本地目录和远程目录
local_path = "G:/ /UKB/ukb-0603-5.4T"
remote_path = "/mnt/data3/ukb-0603-5.4T"

# 筛选条件，例如只复制特定扩展名的文件
# files_to_copy = [f for f in os.listdir(local_path) if f.endswith('.yaml')]

# 复制文件到远程服务器
# for file_name in files_to_copy:
#     local_file_path = os.path.join(local_path, file_name)
#     try:
#         scp_client.put(local_file_path, os.path.join(remote_path, file_name), recursive=True)
#     except Exception as e:
#         print(f"Error copying {file_name}: {e}")

scp_client.put(local_path, remote_path, recursive=True)

# 关闭连接
scp_client.close()
ssh_client.close()