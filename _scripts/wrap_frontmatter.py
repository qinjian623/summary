import os
import re
from pathlib import Path
from datetime import datetime

SRC_ROOT = Path("_raw_output")
DST_ROOT = Path("_posts")

DST_ROOT.mkdir(exist_ok=True)


def safe_filename(base_name, ext=".md"):
    """避免文件重名，自动加数字后缀"""
    dst = DST_ROOT / f"{base_name}{ext}"
    idx = 1
    while dst.exists():
        dst = DST_ROOT / f"{base_name}-{idx}{ext}"
        idx += 1
    return dst


for root, _, files in os.walk(SRC_ROOT):
    root_path = Path(root)
    if root_path == SRC_ROOT:
        continue  # 跳过 output 根目录本身

    folder_name = root_path.name  # 以子目录名作为输出 md 名

    for f in files:
        if not f.endswith(".md"):
            continue

        src_path = root_path / f
        with open(src_path, "r", encoding="utf-8") as fp:
            txt = fp.read()

        mp3_path = root_path / "audio.mp3"

        if os.path.exists(mp3_path):
            # 获取 mp3 文件的创建时间
            ctime = os.path.getctime(mp3_path)
            date_str = datetime.fromtimestamp(
                ctime).strftime("%Y-%m-%d-%H:%M:%S")
            # print(date_str)
        else:
            ctime = os.path.getctime(src_path)
            date_str = datetime.fromtimestamp(
                ctime).strftime("%Y-%m-%d-%H:%M:%S")

            # 构造目标文件路径
        dst_path = safe_filename(date_str + folder_name)

        # 如果没有 front matter，就加上
        if not txt.startswith("---"):
            date_str = ""
            # mp3_path = md path 同目录下的 audio.mp3

            # print(os.path.exists(mp3_path))

            # print(mp3_path)
            print(date_str)
            front = "---\nlayout: default\n"
            if date_str:
                front += f"cdate: {date_str}\n"
            front += "---\n\n"

            txt = front + txt
        if not os.path.exists(dst_path):
            with open(dst_path, "w", encoding="utf-8") as fp:
                fp.write(txt)

            # print(f"{src_path}  -->  {dst_path}")
