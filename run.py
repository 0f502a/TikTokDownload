# 根据uid_list.txt批量下载抖音用户视频
# 2023/05/02: 要求每一行格式为[url短链 + '\t' + 用户名]
import Util
import os
import time
from datetime import datetime
import random


if __name__ == "__main__":
    cfg = Util.Config()
    cfg = cfg.check()  # 读取conf.ini的配置

    # uid = cfg.get('uid', 'uid')
    path = cfg.get('path', 'path')
    mode = cfg.get('mode', 'mode')
    music = cfg.get('music', 'music')
    cookie = cfg.get('cookie', 'cookie')
    interval = cfg.get('interval', 'interval')
    update = cfg.get('update', 'update')

    sleep_secs = 2

    users = list()
    with open('uid_list.txt', 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            users.append(
                (line[0], line[1])  # a tuple: (uid, uname)
            )
    random.shuffle(users)  # 打乱下载列表

    for i, (uid, uname) in enumerate(users):
        print(">>>")
        print(f"   [{datetime.now()}]下载进度: {i+1}/{len(users)}, 正在下载用户[{uname} - {uid}]")

        # python TikTokTool.py --uid "https://v.douyin.com/DgYeM6G/" --path "../Download/" --mode "post" 
        os.system(f'python TikTokTool.py --uid {uid} --path {path} --mode {mode} --cookie "{cookie}"')

        print(f"完成一名用户[{uname}]的视频下载，{sleep_secs}秒后开始下一用户。")
        time.sleep(sleep_secs)

    print("全部用户下载完成")
    exit(0)
