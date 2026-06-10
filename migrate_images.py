import os
import re
import shutil
import sys
from collections import defaultdict

# ========== 配置 ==========
CONTENT_DIR = "content"
POSTS_DIR = os.path.join(CONTENT_DIR, "posts")
UPLOADS_DIR = os.path.join(CONTENT_DIR, "uploads")
OLD_DOMAIN = "cxiansheng.cn/usr/uploads/"
# ==========================

def find_all_index_md():
    """递归查找所有 index.md 文件"""
    matches = []
    for root, dirs, files in os.walk(POSTS_DIR):
        if 'index.md' in files:
            matches.append(os.path.join(root, 'index.md'))
    return matches

def extract_image_refs(md_file):
    """从 index.md 中提取所有旧图片 URL 路径"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # 匹配 http://cxiansheng.cn/usr/uploads/ 后面的路径，支持 https 和域名变体
    pattern = re.compile(r'https?://cxiansheng\.cn/usr/uploads/([^"\')\s]+)')
    matches = pattern.findall(content)
    # 返回列表，每个元素是相对路径如 "2016/11/2844619032.png"
    return matches

def locate_image_in_uploads(rel_path):
    """在 uploads 目录下根据相对路径查找图片"""
    local_path = os.path.join(UPLOADS_DIR, rel_path)
    if os.path.isfile(local_path):
        return local_path
    return None

def preview():
    """预览模式：收集所有需要迁移的信息，不实际修改"""
    index_files = find_all_index_md()
    if not index_files:
        print("未找到任何 index.md 文件")
        return

    results = defaultdict(list)  # key: 文章文件夹路径, value: 列表，每项为 (旧URL路径, 本地图片绝对路径, 图片文件名)

    for md_file in index_files:
        folder = os.path.dirname(md_file)
        refs = extract_image_refs(md_file)
        if not refs:
            continue
        for rel_path in refs:
            src_img = locate_image_in_uploads(rel_path)
            if src_img:
                img_filename = os.path.basename(rel_path)
                results[folder].append((rel_path, src_img, img_filename))
            else:
                print(f"⚠️  警告: 在 {md_file} 中找不到图片 {rel_path}，请检查 uploads 目录")

    if not results:
        print("没有找到任何可迁移的图片引用")
        return

    print("\n========== 预览结果 ==========\n")
    for folder, items in results.items():
        print(f"📁 文章文件夹: {folder}")
        for rel_path, src_img, img_filename in items:
            print(f"   🖼️  旧引用: {rel_path}")
            print(f"      源文件: {src_img}")
            print(f"      将移动到: {folder}/{img_filename}")
            print()
    print(f"共发现 {sum(len(v) for v in results.values())} 张图片需要迁移")
    print("预览完成。如需执行迁移，请运行: python migrate_images.py --apply")

def apply():
    """执行模式：实际移动文件并修改引用"""
    index_files = find_all_index_md()
    if not index_files:
        print("未找到任何 index.md 文件")
        return

    total_moved = 0
    for md_file in index_files:
        folder = os.path.dirname(md_file)
        refs = extract_image_refs(md_file)
        if not refs:
            continue
        # 读取文件内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        modified = False
        for rel_path in refs:
            src_img = locate_image_in_uploads(rel_path)
            if not src_img:
                print(f"⚠️  跳过: {md_file} 中 {rel_path} 不存在")
                continue
            img_filename = os.path.basename(rel_path)
            dst_img = os.path.join(folder, img_filename)
            # 移动文件（如果目标已存在，先备份？暂不处理，直接覆盖）
            if not os.path.exists(dst_img):
                shutil.move(src_img, dst_img)
                print(f"✅ 移动: {src_img} -> {dst_img}")
            else:
                print(f"⚠️  目标已存在，跳过移动: {dst_img}")
            # 替换内容中的 URL
            old_url = f"http://{OLD_DOMAIN}{rel_path}"
            # 也替换 https 的情况
            old_url_https = f"https://{OLD_DOMAIN}{rel_path}"
            new_ref = f"./{img_filename}"
            content = content.replace(old_url, new_ref)
            content = content.replace(old_url_https, new_ref)
            modified = True
            total_moved += 1
        if modified:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 已更新: {md_file}")
    print(f"\n完成！共移动并更新 {total_moved} 张图片。")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--apply':
        apply()
    else:
        preview()

if __name__ == "__main__":
    main()