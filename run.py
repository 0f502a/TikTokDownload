# 根据uid_list.txt批量下载抖音用户视频
import Util
import os
import time

cfg = Util.Config()
cfg = cfg.check()  # 读取conf.ini的配置

# uid = cfg.get('uid', 'uid')
path = cfg.get('path', 'path')
mode = cfg.get('mode', 'mode')
music = cfg.get('music', 'music')
cookie = cfg.get('cookie', 'cookie')
interval = cfg.get('interval', 'interval')
update = cfg.get('update', 'update')

sleep_secs = 5

with open('uid_list.txt', 'r') as f:
    n = len(f.readlines())
with open('uid_list.txt', 'r') as f:
    for i, line in enumerate(f.readlines()):
        print(">>>")
        print(f"   下载进度: {i+1}/{n}")
        uid = line.strip()
        os.system(f'python TikTokTool.py --uid {uid} --path {path} --mode {mode} --cookie "{cookie}"')
        print(f"完成一名用户视频的下载，{sleep_secs}秒后开始下一用户。")
        time.sleep(sleep_secs)

print("全部用户下载完成")
exit(0)
