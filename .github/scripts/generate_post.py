import os
import json
import random
from datetime import datetime
import openai
from slugify import slugify
import frontmatter
from pathlib import Path

# 配置 OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')
if os.getenv('OPENAI_API_ORG'):
    openai.organization = os.getenv('OPENAI_API_ORG')

# 文章主题和分类映射
TOPICS = {
    "技术趋势": {
        "topics": ["AI发展趋势", "云原生技术", "Web3.0", "元宇宙", "边缘计算"],
        "category": "技术前沿"
    },
    "编程语言": {
        "topics": ["Python进阶", "Go语言实践", "Rust入门", "JavaScript新特性", "TypeScript最佳实践"],
        "category": "编程语言"
    },
    "后端开发": {
        "topics": ["微服务架构", "分布式系统", "数据库优化", "消息队列", "API设计"],
        "category": "后端开发"
    },
    "前端开发": {
        "topics": ["React Hooks", "Vue3组件", "前端性能优化", "移动端适配", "现代CSS技巧"],
        "category": "前端开发"
    },
    "DevOps": {
        "topics": ["容器化部署", "CI/CD实践", "监控告警", "日志管理", "安全最佳实践"],
        "category": "DevOps"
    }
}

def generate_post_topic():
    """生成文章主题和大纲"""
    category = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[category]["topics"])
    prompt = f"""
    请为技术博客生成一篇关于{topic}的高质量文章大纲，要求：
    1. 文章标题要具体且吸引人
    2. 包含 3-5 个主要部分
    3. 每个部分都要有 2-3 个子要点
    4. 适合技术读者阅读
    请用 JSON 格式返回，包含 title 和 outline 字段
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.choices[0].message.content)

def generate_post_content(outline):
    """根据大纲生成文章内容"""
    prompt = f"""
    请根据以下大纲生成一篇技术博客文章：
    {json.dumps(outline, ensure_ascii=False)}
    
    要求：
    1. 使用 Markdown 格式
    2. 内容专业且具体
    3. 包含实际案例或代码示例
    4. 语气专业但友好
    5. 每个部分都要充实且有见地
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def create_post_file(title, content, category):
    """创建文章文件"""
    now = datetime.now()
    slug = slugify(title)
    filename = f"{now.strftime('%Y-%m-%d')}-{slug}.md"
    
    post = frontmatter.Post(
        content,
        title=title,
        date=now.strftime('%Y-%m-%d'),
        draft=False,
        tags=["AI生成", category, "热门文章"],
        categories=[category],
        author="AI助手",
        featuredImage="",
        toc=True,
        weight=random.randint(1, 100)  # 用于排序
    )
    
    posts_dir = Path('content/posts')
    posts_dir.mkdir(parents=True, exist_ok=True)
    
    with open(posts_dir / filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

def main(num_posts=20):
    # 设置要生成的文章数量
    num_posts = int(num_posts)
    
    # 记录已生成的主题，避免重复
    generated_topics = set()
    
    for _ in range(num_posts):
        # 生成文章主题和大纲
        post_data = None
        category = None
        
        # 确保主题不重复
        while True:
            category = random.choice(list(TOPICS.keys()))
            post_data = generate_post_topic()
            if post_data['title'] not in generated_topics:
                generated_topics.add(post_data['title'])
                break
        
        # 生成文章内容
        content = generate_post_content(post_data)
        
        # 创建文章文件
        create_post_file(post_data['title'], content, TOPICS[category]['category'])
        
        # 等待一小段时间，避免API限制
        time.sleep(1)

if __name__ == '__main__':
    import time
    import sys
    num_posts = sys.argv[1] if len(sys.argv) > 1 else 20
    main(num_posts)
