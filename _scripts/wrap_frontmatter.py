import os
import re
from pathlib import Path

SRC_ROOT = Path("_raw_output")
DST_ROOT = Path("_posts")
FRONT = "---\nlayout: default\n---\n\n"

DST_ROOT.mkdir(exist_ok=True)

def safe_filename(base_name, ext=".md"):
    """避免文件重名，自动加数字后缀"""
    dst = DST_ROOT / f"0001-01-01-{base_name}{ext}"
    idx = 1
    while dst.exists():
        dst = DST_ROOT / f"0001-01-01-{base_name}-{idx}{ext}"
        idx += 1
    return dst

for root, _, files in os.walk(SRC_ROOT):
    root_path = Path(root)
    if root_path == SRC_ROOT:
        continue  # 跳过 output 根目录本身

    folder_name = root_path.name  # 以子目录名作为输出 md 名

    for f in files:
        if f.endswith(".md"):
            src_path = root_path / f
            with open(src_path, "r", encoding="utf-8") as fp:
                txt = fp.read()

            # 构造目标文件路径
            dst_path = safe_filename(folder_name)

            # 如果没有 front matter，就加上
            if not txt.startswith("---"):
                txt = FRONT + txt

            with open(dst_path, "w", encoding="utf-8") as fp:
                fp.write(txt)

            print(f"{src_path}  -->  {dst_path}")
