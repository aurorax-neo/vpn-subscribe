# 定义访问令牌，仓库名称和文件夹路径
import requests

token = '*****'
repo = 'aurorax-neo/vpn-subscribe'
folder_path = 'config'

# 定义 API 端点
api_endpoint = f"https://api.github.com/repos/{repo}/contents/{folder_path}?ref=subscribe"

# 定义头部信息
headers = {'Authorization': f'token {token}'}

# 向 API 端点发送 GET 请求
response = requests.get(api_endpoint, headers=headers)

# 检查响应
if response.status_code == 200:
    # 解析 JSON 响应
    data = response.json()

    # 遍历文件夹中的所有文件
    for file in data:
        # 打印文件链接
        print("https://mirror.ghproxy.com/" + file['download_url'] + "\n")
else:
    print(f"获取文件失败。状态码：{response.status_code}")
