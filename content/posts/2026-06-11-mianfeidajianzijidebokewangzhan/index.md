---
date: '2026-06-11T20:11:16+08:00'
title: '不需要服务器，免费搭建自己的博客网站'
categories: ["后端"]
tags: ["gitHub pages", "博客搭建"]
featured: false
draft: false
---

# 不需要服务器，免费搭建自己的博客网站

## 从 Typecho 迁移到 GitHub Pages 的完整记录

### 前言

我的云服务器到期了。上面跑着一个 Typecho 博客，文章不多，撑死几十篇。续费一年几百块，就为了托管一堆静态 HTML 页面 —— 怎么算都亏。

于是决定搬家。新方案的要求很简单：不花钱、不用维护服务器、写文章不费劲。

最终选了 **GitHub Pages + Hugo**。这篇文章记录整个迁移过程，踩过的坑和处理思路都写清楚。如果你也打算把自己博客从动态系统迁出来，直接照着来就行。

<!--more-->
---

### 为什么是 Hugo + GitHub Pages？

备选方案不少。Hexo 生态成熟但构建慢，VuePress 偏文档站点，Jekyll 是 GitHub Pages 亲儿子但本地环境折腾人。

Hugo 几个优点戳中我：

- **单个二进制文件**，Go 写的，安装就一行命令，不折腾 Node 版本
- **构建极快**，几十篇文章不到一秒，Hexo 同等量级可能要十几秒
- **Page Bundles** 原生支持，图片和 markdown 放一个文件夹，不用单独管理静态资源目录
- 主题虽然不如 Hexo 多，但够用

配上 GitHub Pages，部署就是一个 `git push`。GitHub Actions 自动构建，全球 CDN 分发，自定义域名支持 HTTPS —— 一分钱不花。

至于 WordPress/Typecho 这类动态博客，个人用其实属于过度设计。数据库、PHP 版本、安全补丁、后台登录 —— 每个都是心智负担。除非你需要评论系统或复杂交互，否则静态方案完全够用。

---

### 一、迁移思路

三步走：

1. **导出数据** —— 从 Typecho 把文章捞出来，转成 Markdown
2. **本地搭建** —— Hugo 建站，导入文章，处理图片和元数据
3. **部署上线** —— 推到 GitHub Pages，绑域名，开 HTTPS

下面按顺序展开，重点说容易出问题的地方。

---

### 二、从 Typecho 导出文章

GitHub 上有个 **typecho-to-markdown** 工具，能直接从 Typecho 数据库批量导出Markdown文件，每个文件都带Front Matter 元数据。跑完之后目录长这样：

```
posts/
├── 2019-05-30.md
├── 2021-03-03.md
└── 2025-04-10.md
```

每个文件头部自带 Front Matter：

```yaml
---
title: "文章标题"
date: 2019-05-30T21:16:00.000Z
slug: article-slug
tags: [随笔]
---
```

导出这一步基本上无痛，但是麻烦的在后面。

---

### 三、搭建 Hugo

#### 3.1 安装

各平台都一行命令的事：

- **Windows**：`scoop install hugo-extended`
- **Mac**：`brew install hugo`
- **Linux**：`sudo apt install hugo`

注意装 **extended** 版，有些主题编译 SCSS 需要它。

#### 3.2 创建站点

```bash
hugo new site my-blog
cd my-blog
git init
```

#### 3.3 选主题

我用了 **hugo-theme-next**，就是 Hexo 那个 NexT 主题的 Hugo 移植版，简洁耐看。如果你喜欢其他风格，PaperMod 和 Stack 也都不错。

用 git submodule 管理主题，方便后续升级：

```bash
git submodule add https://github.com/hugo-next/hugo-theme-next.git themes/hugo-theme-next
```

`hugo.yaml` 里指定主题：

```yaml
theme: hugo-theme-next
```

#### 3.4 导入文章

把导出的 `.md` 文件扔进 `content/posts/`，先不管格式，让 Hugo 跑起来再说。

---

### 四、处理图片 —— 整个迁移最头疼的部分

Typecho 的图片存在 `uploads/` 下，按年/月分目录。文章里引用的是完整 URL：

```markdown
![图片描述](https://你的域名/usr/uploads/2016/11/2844619032.png)
```

问题来了：服务器已经没了，这些 URL 全部 404。我得把所有图片**下载到本地，塞进对应文章的文件夹，再把引用路径改成相对路径**。

手工干不现实，写了个 Python 脚本自动处理：

```python
# 匹配旧域名图片 URL
pattern = re.compile(r'https?://cxiansheng\.cn/usr/uploads/([^"\')\s]+)')

# 逐个处理：
# 1. 找到本地 uploads/ 目录中对应的图片文件
# 2. 复制到文章所在文件夹
# 3. 把文章中的绝对路径引用替换为 ./图片名.png
```

脚本跑完，每篇文章的目录结构变成这样：

```
posts/文章slug/
├── index.md
└── 图片1.png
```

这就是 Hugo 的 **Page Bundles** —— 文章和图片绑在一起，挪目录、改 slug 都不怕链接断。比 Typecho 那种统一 `uploads/` 目录的方式清爽得多。

一个小坑：有些图片文件名带特殊字符或中文，Windows 下要额外处理编码。如果你全程在 Linux/Mac 上操作，不存在这个问题。

---

### 五、处理分类和标签

使用**typecho-to-markdown** 导出的Front Matter 元数据没有分类，标签页不完整，这时候可以写个SQL来取出标题对应的分类和标签，再写个脚本匹配文章标题，批量往 Front Matter 里补 `categories` 和 `tags`；脚本我放到最后。补全分类和标签的元数据如下

```yaml
---
title: "文章标题"
date: 2026-01-24T11:23:00+00:00
categories: ["后端"]
tags: ["php", "协程", "并发编程"]
---
```

两个脚本加起来不到 100 行。迁移这种事，能自动化的就别手操。

---

### 六、Hugo 配置

#### 6.1 `hugo.yaml` 基础配置

```yaml
baseURL: https://www.cxiansheng.cn/
title: 命中水、
theme: hugo-theme-next
locale: zh-cn

[params]
  mainSections = ["posts"]
  archives = { enabled = true }

[menu]
  [[menu.main]]
    name = "首页"
    url = "/"
    weight = 1
  [[menu.main]]
    name = "前端"
    url = "/categories/前端/"
    weight = 2
  [[menu.main]]
    name = "后端"
    url = "/categories/后端/"
    weight = 3
  [[menu.main]]
    name = "归档"
    url = "/archive/"
    weight = 4
  [[menu.main]]
    name = "关于"
    url = "/about/"
    weight = 5
```

菜单项根据你的分类来调，我主要写前端和后端，所以分了两个入口。

#### 6.2 关于页

直接建 `content/about.md`，普通的 Markdown 文件，随便写。

---

### 七、部署到 GitHub Pages

#### 7.1 建仓库

创建一个名为 `<你的用户名>.github.io` 的**公开**仓库。必须是 public，除非你开了 GitHub Pro（Pro 支持私有仓库的 Pages）。

#### 7.2 GitHub Actions 自动部署

在项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy Hugo Site to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.163.0'
          extended: true

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

几个关键点：

- `submodules: recursive` **必须加**，否则 git submodule 引入的主题不会被 checkout，构建直接报错
- `peaceiris/actions-gh-pages@v4` 会把 `./public` 目录推到 `gh-pages` 分支，GitHub Pages 从那个分支读内容
- `hugo-version` 写死一个具体版本号，避免某天 CI 突然拉取新版 Hugo 导致构建行为变化

#### 7.3 推送

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

推送后去仓库的 Actions 标签页看构建进度。成功了就访问 `https://<用户名>.github.io`。

---

### 八、绑定自定义域名

#### 8.1 DNS 解析

在域名服务商加一条 CNAME 记录：

| 记录类型 | 主机记录 | 记录值               |
| -------- | -------- | -------------------- |
| CNAME    | www      | 你的用户名.github.io |

如果你想把 apex domain（不带 www 的裸域名）也指向博客，需要用 A 记录指向 GitHub Pages 的 IP。但 GitHub 的 IP 偶尔会变，更稳妥的做法是统一用 www 子域名，然后做 301 跳转。

#### 8.2 GitHub 侧配置

仓库 **Settings → Pages → Custom domain**，填入 `www.你的域名`，保存。

#### 8.3 CNAME 文件

GitHub 有个烦人的问题：每次部署后 Custom domain 设置可能丢失。解决方法是在 `static/` 目录下放一个 `CNAME` 文件，内容是：

```
www.cxiansheng.cn
```

这样每次构建生成的站点根目录都带着这个文件，GitHub 自动识别。

#### 8.4 HTTPS

DNS 生效后，勾选 **Enforce HTTPS**。GitHub 通过 Let's Encrypt 自动签发证书，不用自己操心续期。

---

### 九、遇到的几个坑

#### 9.1 列表页摘要被截断

Hugo 默认取 `<!--more-->` 之前的内容作为摘要。如果文章没写这个标记，Hugo 会按字数自动截断，经常断在奇怪的位置。

解决：在需要断开的地方手动加 `<!--more-->`。

#### 9.2 分类页菜单不高亮

点进 `/categories/前端/` 后，顶部菜单栏的"前端"没有高亮。原因是主题模板只判断了 `section` 类型，没处理 `term`（分类术语页）。

在主题的 `menu.html` 里找到判断条件，加上 `or .Kind == "term"` 就行。

#### 9.3 端口冲突

`hugo server` 默认 1313。如果被占用了，Hugo 会自动切到 1314、1315……看终端输出确认实际端口就行，不是 bug。

#### 9.4 配置项更名

Hugo v0.158.0 起 `languageCode` 改成了 `locale`，`languageName` 改成了 `label`。如果启动时有 warning 提示字段过期，照提示改过来就行，一分钟的事。

---

### 十、总结

整个迁移花了大半天，大头耗在处理图片和调配置上。迁移之后：

- 服务器费用归零
- 写文章就是本地写 Markdown → `git push`，不用登录后台
- 所有内容在 GitHub 仓库里，换电脑随时 clone 继续写
- GitHub Pages 全球 CDN，国内访问速度也还行

如果你也在维护一个访问量不大的动态博客，值得花一个周末迁出来。静态博客的维护成本低到几乎为零，这对个人博客来说就是最好的特性。

---

### 十一、处理脚本

#### 11.1 脚本一：文章分层脚本

**文件名**：`migrate_to_page_bundles.py`

**目标**：将 `.md` 文件转换为文件夹 + `index.md` 结构

**功能**：

- 读取 `posts/` 目录下的 `.md` 文件
- 提取文章的 `slug`（如果没有则用文件名）
- 创建以 `slug` 命名的文件夹
- 将文章重命名为 `index.md` 移入该文件夹
- 可选：删除原 `.md` 文件（默认注释，需手动取消注释）

```python
import os
import re
import shutil

# ========== 配置 ==========
POSTS_DIR = "posts"          # 存放 .md 文章的文件夹
# ==========================

def get_slug_from_md(filepath):
    """从 Markdown 文件的 front matter 中提取 slug 字段"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
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

    # 4. 将文章内容写入 index.md
    index_file = os.path.join(target_dir, "index.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  生成 index.md: {index_file}")

    # 5. 删除原 .md 文件（可选，确认无误后取消注释）
    # os.remove(md_file)
    # print(f"  删除原文件: {md_file}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"错误：找不到 '{POSTS_DIR}' 文件夹")
        return

    md_files = [f for f in os.listdir(POSTS_DIR) 
                if f.endswith('.md') and os.path.isfile(os.path.join(POSTS_DIR, f))]
    if not md_files:
        print("没有找到 .md 文件。")
        return

    print(f"找到 {len(md_files)} 篇文章，开始处理...")
    for md_file in md_files:
        full_path = os.path.join(POSTS_DIR, md_file)
        process_article(full_path)

    print("\n全部处理完成！")
    print("请检查生成的文件夹和 index.md，确认无误后再手动删除原始 .md 文件")

if __name__ == "__main__":
    main()
```

#### 11.2 脚本二：图片资源移动到 `index.md` 同级目录

**文件名**：`migrate_images.py`

**功能**：

- 扫描所有 `index.md` 中的旧域名图片引用
- 在 `content/uploads/` 下找到对应图片
- 将图片复制到文章文件夹（与 `index.md` 同级）
- 修改 `index.md` 中的引用为相对路径 `./图片名.png`

```python
import os
import re
import shutil
import sys

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
    pattern = re.compile(r'https?://cxiansheng\.cn/usr/uploads/([^"\')\s]+)')
    return pattern.findall(content)

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

    results = {}
    for md_file in index_files:
        folder = os.path.dirname(md_file)
        refs = extract_image_refs(md_file)
        if not refs:
            continue
        results[folder] = []
        for rel_path in refs:
            src_img = locate_image_in_uploads(rel_path)
            if src_img:
                img_filename = os.path.basename(rel_path)
                results[folder].append((rel_path, src_img, img_filename))
            else:
                print(f"⚠️  警告: 在 {md_file} 中找不到图片 {rel_path}")

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

            if not os.path.exists(dst_img):
                shutil.move(src_img, dst_img)
                print(f"✅ 移动: {src_img} -> {dst_img}")
            else:
                print(f"⚠️  目标已存在，跳过移动: {dst_img}")

            old_url = f"http://{OLD_DOMAIN}{rel_path}"
            old_url_https = f"https://{OLD_DOMAIN}{rel_path}"
            content = content.replace(old_url, f"./{img_filename}")
            content = content.replace(old_url_https, f"./{img_filename}")
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
```

#### 11.3 脚本三：根据 JSON 更新 `index.md` 中的 `categories` 和 `tags`

**文件名**：`update_categories_tags.py`

**功能**：

- 读取 JSON 数据（每篇文章的标题、分类、标签）
- 根据标题匹配 `index.md` 文件
- 更新或添加 `categories` 和 `tags` 字段

**JSON 数据格式示例**（保存为 `categories_tags.json`）：

```json
[
  {
    "title": "Laravel + Swoole 协程实战：一个多租户采集系统的真实落地方案",
    "type": "category",
    "name": "后端",
    "slug": "server"
  },
  {
    "title": "Laravel + Swoole 协程实战：一个多租户采集系统的真实落地方案",
    "type": "tag",
    "name": "php",
    "slug": "php"
  },
  {
    "title": "Laravel + Swoole 协程实战：一个多租户采集系统的真实落地方案",
    "type": "tag",
    "name": "协程",
    "slug": "协程"
  }
]
```

```python
import os
import json
import sys
from collections import defaultdict

# ========== 配置 ==========
POSTS_DIR = "content/posts"
JSON_FILE = "categories_tags.json"
# ==========================

def load_json_data(json_path):
    """加载 JSON 文件，返回按 title 分组的数据"""
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

def find_all_index_md():
    """递归查找所有 index.md 文件"""
    matches = []
    for root, dirs, files in os.walk(POSTS_DIR):
        if 'index.md' in files:
            matches.append(os.path.join(root, 'index.md'))
    return matches

def extract_title_from_md(filepath):
    """从 index.md 中提取 front matter 的 title"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    front_matter = parts[1]
    for line in front_matter.split('\n'):
        if line.strip().startswith('title:'):
            title = line.split(':', 1)[1].strip()
            # 去掉可能的引号
            if (title.startswith('"') and title.endswith('"')) or \
               (title.startswith("'") and title.endswith("'")):
                title = title[1:-1]
            return title
    return None

def update_file(filepath, categories, tags, dry_run=True):
    """更新 index.md 中的 categories 和 tags 字段"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    front = parts[1]
    body = parts[2]

    lines = front.split('\n')
    new_lines = []
    has_categories = False
    has_tags = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('categories:'):
            has_categories = True
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}categories: {json.dumps(list(categories), ensure_ascii=False)}")
            i += 1
            # 跳过多行数组（如果存在）
            while i < len(lines) and (lines[i].startswith('  ') or lines[i].startswith('\t')):
                i += 1
            continue

        if stripped.startswith('tags:'):
            has_tags = True
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}tags: {json.dumps(list(tags), ensure_ascii=False)}")
            i += 1
            while i < len(lines) and (lines[i].startswith('  ') or lines[i].startswith('\t')):
                i += 1
            continue

        new_lines.append(line)
        i += 1

    # 如果缺少 categories 或 tags，在 title 或 date 行后插入
    if not has_categories and categories:
        insert_pos = -1
        for idx, line in enumerate(new_lines):
            if line.strip().startswith('title:') or line.strip().startswith('date:'):
                insert_pos = idx + 1
                break
        if insert_pos == -1:
            insert_pos = 1
        indent = ' ' * 2
        new_lines.insert(insert_pos, f"{indent}categories: {json.dumps(list(categories), ensure_ascii=False)}")

    if not has_tags and tags:
        insert_pos = -1
        for idx, line in enumerate(new_lines):
            if line.strip().startswith('categories:') or line.strip().startswith('title:'):
                insert_pos = idx + 1
                break
        if insert_pos == -1:
            insert_pos = 1
        indent = ' ' * 2
        new_lines.insert(insert_pos, f"{indent}tags: {json.dumps(list(tags), ensure_ascii=False)}")

    new_front = '\n'.join(new_lines)
    new_content = f"---\n{new_front}\n---{body}"

    if dry_run:
        print(f"  [预览] 将更新: {filepath}")
        print(f"    categories: {list(categories)}")
        print(f"    tags: {list(tags)}")
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

    if not os.path.exists(JSON_FILE):
        print(f"错误：找不到 {JSON_FILE}，请将 JSON 数据保存为此文件")
        return

    grouped = load_json_data(JSON_FILE)
    print(f"已加载 {len(grouped)} 个不同标题的数据")

    md_files = find_all_index_md()
    print(f"找到 {len(md_files)} 个 index.md 文件")

    to_update = []
    for filepath in md_files:
        title = extract_title_from_md(filepath)
        if not title:
            continue
        if title in grouped:
            info = grouped[title]
            to_update.append({
                'file': filepath,
                'title': title,
                'categories': sorted(list(info['categories'])),
                'tags': sorted(list(info['tags']))
            })

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
```

#### 11.4 使用说明汇总

| 脚本                         | 用途                             | 运行命令                                                     |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------ |
| `migrate_to_page_bundles.py` | 将 `.md` 转成文件夹 + `index.md` | `python migrate_to_page_bundles.py`                          |
| `migrate_images.py`          | 移动图片到文章文件夹，修改引用   | `python migrate_images.py`（预览）<br>`python migrate_images.py --apply`（执行） |
| `update_categories_tags.py`  | 更新分类和标签                   | `python update_categories_tags.py`（预览）<br>`python update_categories_tags.py --write`（执行） |

**注意**：

- 所有脚本都应放在博客项目根目录（`hugo.yaml` 所在目录）运行
- 运行前建议**备份** `content/posts/` 目录
- 脚本二需要 `content/uploads/` 目录存在
- 脚本三需要准备 `categories_tags.json` 文件

### 附录：相关链接

- [Hugo 官方文档](https://gohugo.io/)
- [GitHub Pages 文档](https://pages.github.com/)
- [hugo-theme-next 主题](https://github.com/hugo-next/hugo-theme-next)

---

*本文首发于 [https://www.cxiansheng.cn](https://www.cxiansheng.cn)*

**作者**：命中水

**版权声明**：转载请注明出处，欢迎技术交流

