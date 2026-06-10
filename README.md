# 命中水、的个人博客

基于 [Hugo](https://gohugo.io/) 静态站点生成器搭建的个人博客，使用 [hugo-theme-next](https://github.com/hugo-next/hugo-theme-next) 主题，通过 GitHub Pages 部署。

在线地址：[https://mingzhongshui.github.io/](https://mingzhongshui.github.io/)

## 项目结构

```
my-blog/
├── archetypes/     # 文章模板
├── assets/         # 自定义资源（CSS/JS）
├── content/        # 博客文章内容
│   └── posts/      # 所有文章存放目录
├── layouts/        # 自定义布局覆盖
├── static/         # 静态文件（图片等）
├── themes/         # 主题子模块（当前使用 hugo-theme-next）
├── hugo.yaml       # Hugo 站点配置
└── public/         # 构建产物（Git 忽略）
```

## 环境要求

- Hugo Extended v0.163+
- Git

## 常用操作指令

### 开发调试

```bash
# 启动本地开发服务器（默认 http://localhost:1313）
hugo server

# 启动并指定端口
hugo server -p 8080

# 启动并包含草稿文章
hugo server -D

# 启动并允许局域网访问
hugo server --bind 0.0.0.0
```

### 文章管理

```bash
# 创建新文章（生成 content/posts/<title>/index.zh-cn.md）
hugo new content posts/文章文件名/index.md

# 新建 Markdown 文件作为 blog（自动使用 archetypes 模板）
hugo new content posts/文章文件名.md
```

### 主题管理

```bash
# 添加新主题（以 git submodule 方式）
git submodule add https://github.com/<作者>/<主题名>.git themes/<主题名>

# 克隆仓库时连带所有主题子模块
git clone --recursive https://github.com/mingzhongshui/mingzhongshui.github.io.git

# 更新所有子模块到最新
git submodule update --remote --merge

# 更新指定子模块
git submodule update --remote themes/hugo-theme-next

# 初始化并拉取所有子模块（已克隆但缺少子模块时）
git submodule update --init --recursive

# 删除子模块
git submodule deinit themes/<主题名>
git rm themes/<主题名>
```

### 构建与部署

```bash
# 构建静态站点（输出到 public/ 目录）
hugo

# 构建并包含草稿文章
hugo -D

# 清理 public 目录后重新构建
hugo --cleanDestinationDir
```

### 其他

```bash
# 检查 Hugo 版本
hugo version

# 查看 Hugo 环境信息
hugo env

# 列出所有草稿文章
hugo list drafts

# 列出所有已发布文章
hugo list published
```

## 部署

本项目通过 GitHub Actions 自动构建并部署到 GitHub Pages，配置文件位于 `.github/workflows/`。推送到 `main` 分支后会自动触发部署。
