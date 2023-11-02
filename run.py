# 根据uid_list.txt批量下载抖音用户视频
# 2023/05/02: 要求每一行格式为[url短链 + '\t' + 用户名]
import Util
import os
import time
from datetime import datetime, timedelta
import random


def get_args():
    # 从命令行获取参数：1.文件路径；2.day_offset
    import argparse
    parser = argparse.ArgumentParser(description='批量下载抖音用户视频')
    parser.add_argument('-f', '--file', type=str, default="uid_list.txt", help='下载文件列表')
    parser.add_argument('-d', '--day_offset', type=int, default=14, help='从今天往前推day_offset天')
    args = parser.parse_args()
    return args.file, args.day_offset


if __name__ == "__main__":
    # 默认配置
    run_cfg = {
        # 配置参数
        "uid_file": "uid_list.txt",
        "day_offset": 14,  # 从今天往前推day_offset天
        "sleep_secs": 2,  # 每下载一名用户的视频后，休息sleep_secs秒再下载下一名用户的视频
        # 下载参数
        "path": "../Download/",
        "mode": "post",
        "music": "no",
        "cookie": "",
        "interval": "all",
        "update": "no"
    }

    # 1. 从命令行获取配置参数
    run_cfg["uid_file"], run_cfg["day_offset"] = get_args()

    # 2. 配置时间范围
    # 如果day_offset > 0，则从今天往前推day_offset天；否则，下载全部视频
    day_offset = run_cfg["day_offset"]
    if day_offset > 0:
        # 获取今天日期，并构建形如2022-01-01|2023-01-01的日期范围字符串
        day_end = datetime.now().strftime("%Y-%m-%d")
        day_start = (datetime.now() - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        interval = f"{day_start}|{day_end}"
        run_cfg["interval"] = interval

    # 3. 配置TiktokTool.py的参数
    cfg = Util.Config()
    cfg = cfg.check()  # 读取conf.ini的配置

    run_cfg["path"] = cfg.get('path', 'path')
    run_cfg["mode"] = cfg.get('mode', 'mode')
    run_cfg["music"] = cfg.get('music', 'music')
    run_cfg["cookie"] = cfg.get('cookie', 'cookie')
    run_cfg["update"] = cfg.get('update', 'update')
    run_cfg["interval"] = run_cfg["interval"]

    # 打印所有配置信息
    print(">>>")
    print(f"   [{datetime.now()}]配置信息如下：")
    for k, v in run_cfg.items():
        print(f"   {k} = {v}")
    print(">>>")

    # 4. 用户列表准备
    users = list()
    with open(run_cfg["uid_file"], 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            users.append(
                (line[0], line[1])  # a tuple: (uid, uname)
            )
    random.shuffle(users)  # 打乱下载列表

    # 5. 开始下载
    for i, (uid, uname) in enumerate(users):
        print(">>>")
        print(f"   [{datetime.now()}]下载进度: {i+1}/{len(users)}, 正在下载用户[{uname} - {uid}]")

        # python TikTokTool.py --uid "https://v.douyin.com/DgYeM6G/" --path "../Download/" --mode "post" 
        cmd = 'python TikTokTool.py -u %s -p %s --mode %s --cookie "%s" --folderize no -I "%s"' % \
            (
             uid, 
             run_cfg["path"], 
             run_cfg["mode"], 
             run_cfg["cookie"], 
             run_cfg["interval"]
            )
        # print(f"   [{datetime.now()}]执行命令: {cmd}")
        os.system(cmd)

        sleep_secs = run_cfg["sleep_secs"]
        print(f"完成一名用户[{uname}]的视频下载，{sleep_secs}秒后开始下一用户。")
        time.sleep(sleep_secs)

    # 下载完成
    print("全部用户下载完成")
    exit(0)