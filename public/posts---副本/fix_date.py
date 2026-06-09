# fix_date.py
import os
import re
from datetime import datetime

# ===== 请在这里配置你的信息 =====
# 如果你文章的日期字段不叫 'date'，请把下面引号里的值改掉，例如 'pubDatetime'
old_date_field = 'pubDatetime'  # <--- 重点检查这里！
# 你的文章所在的文件夹路径
content_dir = '.'  # '.' 代表当前文件夹，你也可以改成具体路径，如 r'E:\code\my-blog\content\posts'
# ==============================

fixed_count = 0
for filename in os.listdir(content_dir):
    if not filename.endswith('.md'):
        continue

    filepath = os.path.join(content_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查front matter中是否存在旧的日期字段
    # 这个正则会匹配 "pubDatetime: 2019-05-30T21:16:00.000Z" 这样的行
    pattern = rf'^{re.escape(old_date_field)}:\s*(.*?)$'
    match = re.search(pattern, content, re.MULTILINE)

    if match:
        old_date_value = match.group(1).strip()
        # 尝试解析各种常见的日期格式
        new_date_value = None
        # 格式1: 2025-04-10T14:40:18+08:00 或 2019-05-30T21:16:00.000Z
        if 'T' in old_date_value:
            try:
                # 解析带时区的ISO格式
                dt = datetime.fromisoformat(old_date_value.replace('Z', '+00:00'))
                new_date_value = dt.isoformat()
            except:
                pass
        # 格式2: 2025-04-10
        elif re.match(r'\d{4}-\d{2}-\d{2}$', old_date_value):
            new_date_value = f"{old_date_value}T00:00:00+08:00"

        if new_date_value:
            # 在front matter中，用标准的 'date' 字段替换旧的字段
            # 先删除旧的字段行，然后在文件开头添加 'date' 字段
            new_content = re.sub(pattern, f'date: {new_date_value}', content, flags=re.MULTILINE)
            # 如果你只是想添加date字段而保留旧的，可以用下面的代码替换上面的行
            # new_content = re.sub(pattern, rf'\g<0>\ndate: {new_date_value}', content, flags=re.MULTILINE)

            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'✓ 已修复: {filename} (将 "{old_date_field}: {old_date_value}" 改为 "date: {new_date_value}")')
            fixed_count += 1
        else:
            print(f'⚠ 无法解析: {filename} 中的日期 "{old_date_value}"')
    else:
        # 检查是否已经有 'date' 字段
        if not re.search(r'^date:', content, re.MULTILINE):
            print(f'⚠ 未找到: {filename} 中没有任何日期字段，请手动添加。')
        else:
            print(f'✓ 无需修复: {filename} 已包含正确的 date 字段')

print(f'\n完成！共修复 {fixed_count} 个文件。')