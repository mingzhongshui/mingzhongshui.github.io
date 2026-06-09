import os
import sys

POSTS_DIR = "posts"  # 你的文章目录

def process_file(filepath):
    print(f"正在处理: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  读取文件失败: {e}")
        return False

    # 检查文件是否以 '---' 开头
    if not lines or lines[0].strip() != '---':
        print(f"  跳过：不是标准的 Front Matter 文件")
        return False

    # 找到第二个 '---' 的位置（Front Matter 的结束）
    end_of_fm_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_of_fm_index = i
            break

    if end_of_fm_index == -1:
        print(f"  警告：未找到 Front Matter 结束符 '---'，跳过")
        return False

    # 分离 Front Matter 和正文
    fm_lines = lines[1:end_of_fm_index]  # 内容行，不包括首尾的 '---'
    body_lines = lines[end_of_fm_index+1:] # 正文行

    # 处理 Front Matter 中的每一行
    new_fm_lines = []
    modified = False
    for line in fm_lines:
        stripped = line.lstrip()
        # 检查是否是 description: 开头的行（忽略前导空格，且前面没有 #）
        if stripped.startswith('description:') and not line.lstrip().startswith('#'):
            # 注释掉这一行（保留原有的缩进）
            new_fm_lines.append('#' + line)
            modified = True
            print(f"  已注释: description 字段")
        else:
            new_fm_lines.append(line)

    # 如果没有修改，直接返回
    if not modified:
        print(f"  未发现需要注释的 description 字段")
        return False

    # 重新组合文件内容
    new_content = '---\n' + ''.join(new_fm_lines) + '---\n' + ''.join(body_lines)

    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  成功更新文件")
        return True
    except Exception as e:
        print(f"  写入文件失败: {e}")
        return False

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"错误：找不到目录 '{POSTS_DIR}'，请确认脚本运行位置正确。")
        return

    count = 0
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                if process_file(full_path):
                    count += 1

    print(f"\n完成！共处理了 {count} 个文件。")

if __name__ == "__main__":
    main()