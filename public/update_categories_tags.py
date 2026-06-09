import os
import json
import sys
import yaml
from collections import defaultdict

# ========== 配置 ==========
POSTS_DIR = "posts"               # 文章目录
JSON_FILE = "categories_tags.json"  # 存放 JSON 数据的文件
# ==========================

def load_json_data(json_path):
    """加载 JSON 文件，返回按 title 分组的数据结构"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    grouped = defaultdict(lambda: {'categories': set(), 'tags': set()})
    for item in data:
        title = item['title']
        typ = item['type']
        name = item['name']
        if typ == 'category':
            grouped[title]['categories'].add(name)
        elif typ == 'tag':
            grouped[title]['tags'].add(name)
    return grouped

def find_all_index_md(root_dir):
    """递归查找所有 index.md 文件"""
    matches = []
    for dirpath, _, filenames in os.walk(root_dir):
        if 'index.md' in filenames:
            full_path = os.path.join(dirpath, 'index.md')
            matches.append(full_path)
    return matches

def extract_title_from_md(filepath):
    """从 index.md 中提取 front matter 的 title"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 简单分割 front matter
    if not content.startswith('---'):
        return None
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    front_matter = parts[1]
    try:
        data = yaml.safe_load(front_matter)
        return data.get('title')
    except:
        return None

def update_file(filepath, new_categories, new_tags, dry_run=True):
    """更新 index.md 中的 categories 和 tags 字段"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        print(f"  跳过（无 front matter）: {filepath}")
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  跳过（front matter 格式错误）: {filepath}")
        return False

    front = parts[1]
    body = parts[2]

    # 按行处理 front matter，保留注释和顺序
    lines = front.splitlines()
    new_lines = []
    has_categories = False
    has_tags = False
    i = 0
    while i < len(lines):
        line = lines[i]
        # 匹配 categories 行（可能被注释，我们不修改注释的行）
        if line.strip().startswith('categories:'):
            has_categories = True
            # 替换整行为新的 categories 列表
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}categories: {json.dumps(new_categories, ensure_ascii=False)}")
            i += 1
            # 跳过可能的多行数组（简单跳过缩进的行），这里假设 categories 是单行数组
            while i < len(lines) and (lines[i].startswith('  ') or lines[i].startswith('\t')):
                i += 1
            continue
        # 匹配 tags 行
        if line.strip().startswith('tags:'):
            has_tags = True
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}tags: {json.dumps(new_tags, ensure_ascii=False)}")
            i += 1
            while i < len(lines) and (lines[i].startswith('  ') or lines[i].startswith('\t')):
                i += 1
            continue
        new_lines.append(line)
        i += 1

    # 如果缺少 categories 或 tags，在合适位置插入（一般放在 title 或 date 之后）
    if not has_categories and new_categories:
        # 寻找 title 或 date 行，在其后插入
        insert_pos = -1
        for idx, line in enumerate(new_lines):
            if line.strip().startswith('title:') or line.strip().startswith('date:'):
                insert_pos = idx + 1
                break
        if insert_pos == -1:
            insert_pos = 1  # 默认放在第二行
        indent = ' ' * 2  # 默认缩进两个空格
        new_lines.insert(insert_pos, f"{indent}categories: {json.dumps(new_categories, ensure_ascii=False)}")

    if not has_tags and new_tags:
        # 找 categories 或 title 行后面
        insert_pos = -1
        for idx, line in enumerate(new_lines):
            if line.strip().startswith('categories:') or line.strip().startswith('title:'):
                insert_pos = idx + 1
                break
        if insert_pos == -1:
            insert_pos = 1
        indent = ' ' * 2
        new_lines.insert(insert_pos, f"{indent}tags: {json.dumps(new_tags, ensure_ascii=False)}")

    new_front = '\n'.join(new_lines)
    new_content = f"---\n{new_front}\n---{body}"

    if dry_run:
        print(f"  [预览] 将更新: {filepath}")
        print(f"    categories: {new_categories}")
        print(f"    tags: {new_tags}")
        return True
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [已更新] {filepath}")
        return True

def main():
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == '--write':
        dry_run = False
        print("⚠️  准备实际写入文件...")
    else:
        print("🔍 预览模式（不会修改文件）。确认无误后请运行: python update_categories_tags.py --write")

    # 1. 加载 JSON
    if not os.path.exists(JSON_FILE):
        print(f"错误：找不到 {JSON_FILE}，请将 JSON 数据保存为此文件")
        return
    grouped = load_json_data(JSON_FILE)
    print(f"已加载 {len(grouped)} 个不同标题的数据")

    # 2. 查找所有 index.md
    md_files = find_all_index_md(POSTS_DIR)
    print(f"找到 {len(md_files)} 个 index.md 文件")

    # 3. 匹配并输出确认列表
    to_update = []
    for filepath in md_files:
        title = extract_title_from_md(filepath)
        if not title:
            print(f"警告：无法读取标题 {filepath}")
            continue
        if title in grouped:
            info = grouped[title]
            categories = sorted(list(info['categories']))
            tags = sorted(list(info['tags']))
            to_update.append({
                'file': filepath,
                'title': title,
                'categories': categories,
                'tags': tags
            })
        else:
            print(f"未匹配到数据: {title}")

    if not to_update:
        print("没有需要更新的文章。")
        return

    print("\n========== 将要更新的文章列表 ==========")
    for item in to_update:
        print(f"标题: {item['title']}")
        print(f"  文件: {item['file']}")
        print(f"  分类: {item['categories']}")
        print(f"  标签: {item['tags']}")
        print()

    if dry_run:
        print("预览结束。如确认无误，请运行: python update_categories_tags.py --write")
    else:
        print("开始实际写入...")
        for item in to_update:
            update_file(item['file'], item['categories'], item['tags'], dry_run=False)
        print("全部更新完成！")

if __name__ == "__main__":
    main()