# 我的个人博客

这是一个使用 Hugo 和 PaperMod 主题构建的个人博客网站。

## 功能特点

- 响应式设计
- 暗黑模式支持
- 文章目录
- 代码高亮
- 搜索功能
- 标签云
- 文章归档
- 阅读时间估算

## 本地开发

1. 克隆仓库：
```bash
git clone --recursive https://github.com/yuanfang1568/repo-082.git
cd repo-082
```

2. 安装 Hugo：
```bash
# Windows (使用 winget)
winget install Hugo.Hugo
```

3. 启动开发服务器：
```bash
hugo server -D
```

4. 访问 http://localhost:1313 查看网站

## 创建新文章

```bash
hugo new content posts/新文章.md
```

## 部署

网站通过 GitHub Actions 自动部署到 GitHub Pages。每次推送到 main 分支时会自动触发部署。

## 许可证

MIT
