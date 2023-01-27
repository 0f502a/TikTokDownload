# 根据uid_list.txt批量下载抖音用户视频

uid = ""
path = "../Download/"
mode = "post"


import os
with open('uid_list.txt', 'r') as f:
    for line in f.readlines():
        uid = line.strip()
        os.system(f"python TikTokTool.py --uid {uid} --path {path} --mode {mode}")
exit(0)