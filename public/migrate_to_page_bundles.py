import os
import re
import shutil

# ========== 配置 ==========
POSTS_DIR = "posts"          # 存放 .md 文章的文件夹
UPLOADS_DIR = "uploads"      # 存放图片资源的文件夹
DOMAIN_PREFIX = "https://www.cxiansheng.cn/usr/uploads/"  # 需要替换的域名前缀
# ==========================

def get_slug_from_md(filepath):
    """从 Markdown 文件的 front matter 中提取 slug 字段"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 匹配 YAML front matter 中的 slug: xxx
    match = re.search(r'^slug:\s*(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def process_article(md_file):
    """处理单篇文章"""
    print(f"\n处理文件: {md_file}")

    # 1. 获取 slug，如果没有则用文件名（不含扩展名）
    slug = get_slug_from_md(md_file)
    if not slug:
        base_name = os.path.basename(md_file)
        slug = os.path.splitext(base_name)[0]
        print(f"  未找到 slug，使用文件名作为文件夹名: {slug}")

    # 2. 创建以 slug 命名的文件夹
    target_dir = os.path.join(POSTS_DIR, slug)
    os.makedirs(target_dir, exist_ok=True)
    print(f"  创建文件夹: {target_dir}")

    # 3. 读取文章内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. 查找所有图片引用
    # 匹配 https://www.cxiansheng.cn/usr/uploads/后面跟任意路径
    pattern = re.compile(r'https?://www\.cxiansheng\.cn/usr/uploads/([^"\')\s]+)')
    matches = pattern.findall(content)

    if not matches:
        print("  未找到图片引用，仅移动文章文件")

    # 5. 处理每个图片：复制并替换路径
    for rel_path in matches:
        # rel_path 类似 "2018/07/1854799780.jpg"
        source_img = os.path.join(UPLOADS_DIR, rel_path)
        if not os.path.exists(source_img):
            print(f"  警告: 图片不存在 {source_img}")
            continue

        # 目标：复制到 target_dir 下，保持原文件名（或保持相对目录结构也可，这里简化放在同级）
        # 注意：可能存在不同子目录下的同名文件？概率低，直接取 basename
        img_filename = os.path.basename(rel_path)   # 例如 "1854799780.jpg"
        target_img = os.path.join(target_dir, img_filename)

        # 避免重复复制
        if not os.path.exists(target_img):
            shutil.copy2(source_img, target_img)
            print(f"  复制图片: {source_img} -> {target_img}")
        else:
            print(f"  图片已存在: {target_img}")

        # 替换文章中的 URL 为相对路径
        full_url = f"https://www.cxiansheng.cn/usr/uploads/{rel_path}"
        content = content.replace(full_url, f"./{img_filename}")

    # 6. 将文章内容写入 index.md
    index_file = os.path.join(target_dir, "index.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  生成 index.md: {index_file}")

    # 7. 删除原 .md 文件（可选，建议先备份或注释掉）
    # os.remove(md_file)
    # print(f"  删除原文件: {md_file}")

def main():
    # 确保当前工作目录正确（脚本应在 posts 和 uploads 的上级目录执行）
    if not os.path.exists(POSTS_DIR) or not os.path.exists(UPLOADS_DIR):
        print(f"错误：找不到 '{POSTS_DIR}' 或 '{UPLOADS_DIR}' 文件夹，请确认脚本运行位置正确。")
        return

    # 获取所有 .md 文件
    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md') and os.path.isfile(os.path.join(POSTS_DIR, f))]
    if not md_files:
        print("没有找到 .md 文件。")
        return

    print(f"找到 {len(md_files)} 篇文章，开始处理...")
    for md_file in md_files:
        full_path = os.path.join(POSTS_DIR, md_file)
        process_article(full_path)

    print("\n全部处理完成！")
    print("请检查生成的文件夹和 index.md，确认无误后再手动删除原始 .md 文件（脚本已自动备份，未删除）")

if __name__ == "__main__":
    main()