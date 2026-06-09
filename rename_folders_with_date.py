import os
import re
import shutil
from datetime import datetime

# ========== 配置 ==========
POSTS_DIR = "posts"          # 文章文件夹所在的目录
DATE_FORMAT = "%Y-%m-%d"     # 文件夹中日期部分的格式，默认 YYYY-MM-DD
SEPARATOR = "-"              # 日期与 slug 之间的分隔符
# ==========================

def extract_date_from_index_md(folder_path):
    """从文件夹中的 index.md 读取 date 字段，返回 YYYY-MM-DD 字符串"""
    index_path = os.path.join(folder_path, "index.md")
    if not os.path.isfile(index_path):
        return None
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 匹配 front matter 中的 date: ... 或 publishDate: ...
    # 支持格式: date: 2019-05-30 或 date: 2019-05-30T21:16:00+08:00
    match = re.search(r'^date:\s*(.*?)$', content, re.MULTILINE)
    if not match:
        # 有些主题可能用 publishDate
        match = re.search(r'^publishDate:\s*(.*?)$', content, re.MULTILINE)
    if not match:
        return None
    date_str = match.group(1).strip()
    # 尝试解析多种格式
    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%d %H:%M:%S"]:
        try:
            dt = datetime.strptime(date_str.split('+')[0].split('.')[0], fmt)
            return dt.strftime(DATE_FORMAT)
        except ValueError:
            continue
    # 如果上面都不行，尝试只取前10个字符（假设是 YYYY-MM-DD）
    if len(date_str) >= 10 and date_str[4] == '-' and date_str[7] == '-':
        return date_str[:10]
    return None

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"错误：找不到目录 '{POSTS_DIR}'，请确认脚本运行位置正确。")
        return

    folders = [f for f in os.listdir(POSTS_DIR)
               if os.path.isdir(os.path.join(POSTS_DIR, f))]
    if not folders:
        print("没有找到任何文件夹。")
        return

    renamed_count = 0
    skipped_count = 0

    for folder in folders:
        old_path = os.path.join(POSTS_DIR, folder)
        # 检查是否已经包含日期前缀（以 YYYY-MM-DD- 开头）
        if re.match(r'^\d{4}-\d{2}-\d{2}' + re.escape(SEPARATOR), folder):
            print(f"跳过：{folder} 已包含日期前缀")
            skipped_count += 1
            continue

        # 提取日期
        date_prefix = extract_date_from_index_md(old_path)
        if not date_prefix:
            print(f"警告：{folder} 中的 index.md 没有有效的 date 字段，跳过")
            skipped_count += 1
            continue

        new_name = f"{date_prefix}{SEPARATOR}{folder}"
        new_path = os.path.join(POSTS_DIR, new_name)

        if os.path.exists(new_path):
            print(f"错误：目标文件夹 {new_name} 已存在，跳过 {folder}")
            skipped_count += 1
            continue

        # 重命名
        shutil.move(old_path, new_path)
        print(f"✓ 重命名：{folder} -> {new_name}")
        renamed_count += 1

    print(f"\n完成！共重命名 {renamed_count} 个文件夹，跳过 {skipped_count} 个。")

if __name__ == "__main__":
    main()