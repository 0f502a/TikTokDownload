# 根据uid_list.txt批量下载抖音用户视频
# 2023/05/02: 要求每一行格式为[url短链 + '\t' + 用户名]
import os
import time
import random
from rich.console import Console
from datetime import datetime, timedelta
import Util


split_line = "=" * 80
dt = datetime.now().strftime("%Y-%m-%d")
log = Util.Log(file_name=f"run_{dt}.log")
console = Console()


def print_and_log(msg, level="info"):
    console.print(msg)
    if level == "info":
        log.info(msg)
    elif level == "error":
        log.error(msg)
    elif level == "warning":
        log.warning(msg)
    else:
        log.debug(msg)


def get_args():
    # 从命令行获取参数：1.文件路径；2.day_offset
    import argparse
    parser = argparse.ArgumentParser(description='批量下载抖音用户视频')
    parser.add_argument('-f', '--file', type=str, default="uid_list.txt", help='下载文件列表')
    parser.add_argument('-d', '--day_offset', type=int, default=14, help='从今天往前推day_offset天')
    parser.add_argument('-r', '--retry_times', type=int, default=1, help='下载失败后，重试retry_times次')
    args = parser.parse_args()
    return args


def parse_config() -> dict:
    # 默认配置
    run_cfg = {
        # 配置参数
        "uid_file": "uid_list.txt",
        "day_offset": 14,  # 从今天往前推day_offset天
        "sleep_secs": 2,  # 每下载一名用户的视频后，休息sleep_secs秒再下载下一名用户的视频
        "retry_times": 1,  # 下载失败后，重试retry_times次
        # 下载参数
        "path": "../Download/",
        "mode": "post",
        "music": "no",
        "cookie": "",
        "interval": "all",
        "update": "no"
    }

    # 1. 从命令行获取配置参数
    args = get_args()
    run_cfg["uid_file"] = args.file
    run_cfg["day_offset"] = args.day_offset
    run_cfg["retry_times"] = args.retry_times

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

    return run_cfg


def do_download(uid, run_cfg) -> int:
    # example: python TikTokTool.py --uid "https://v.douyin.com/DgYeM6G/" --path "../Download/" --mode "post" 
    cmd = 'python TikTokTool.py -u %s -p %s --mode %s --cookie "%s" --folderize no -I "%s"' % \
        (
            uid, 
            run_cfg["path"], 
            run_cfg["mode"], 
            run_cfg["cookie"], 
            run_cfg["interval"]
        )
    return os.system(cmd)


def do_list_download(users, run_cfg):
    """
    users: List [(uid, uname), ...)]
    run_cfg: dict
    """
    fail_users = list() # 记录下载失败的用户
    for i, (uid, uname) in enumerate(users):
        print_and_log(split_line)
        print_and_log(f"下载进度: {i+1}/{len(users)}, 正在下载用户[{uname} - {uid}]")
        res = do_download(uid, run_cfg)
        if res == 0:
            print_and_log(f"用户[{uname}]的视频下载完成")
        else:
            print_and_log(f"用户[{uname}]的视频下载失败", level="error")
            fail_users.append((uid, uname)) # 记录下载失败的用户
        time.sleep(random.randint(1, 5)) # 随机休眠1-5秒
    return fail_users


def main():
    # 解析配置文件
    run_cfg = parse_config()
    print_and_log("开始下载")
    log.info(f"配置信息如下：")
    for k, v in run_cfg.items():
        log.info(f"{k} = {v}")

    # 用户列表准备
    users, failed_users = list(), list()
    with open(run_cfg["uid_file"], 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            users.append(
                (line[0], line[1])  # a tuple: (uid, uname)
            )
    random.shuffle(users)  # 打乱下载列表

    # 开始下载
    failed_users = do_list_download(users, run_cfg)
    while run_cfg.get("retry_times", 0) > 0 and len(failed_users) > 0:
        print_and_log(split_line)
        print_and_log("开始重试下载失败的用户")
        failed_users = do_list_download(failed_users, run_cfg)
        run_cfg["retry_times"] -= 1

    # 下载完成
    print_and_log("全部用户下载完成")
    print_and_log("下载成功 {} 个用户".format(len(users) - len(failed_users)))
    print_and_log("下载失败 {} 个用户".format(len(failed_users)))
    if len(failed_users) > 0:
        log.info("失败用户列表如下：")
        for uid, uname in failed_users:
            log.info(f"{uname} - {uid}")
        # 保存下载失败列表
        fail_folder = "./uid_list/failed/"
        if not os.path.exists(fail_folder):
            os.makedirs(fail_folder)
        fail_txt = f"failed_users_{dt}.txt"
        with open(fail_folder+fail_txt, 'w', encoding='utf8') as f:
            for uid, uname in failed_users:
                f.write(f"{uid}\t{uname}\n")
        print_and_log("下载失败列表已保存至{}".format(fail_txt))
    
    print_and_log("下载完毕")
    exit(0)

if __name__ == "__main__":
    main()