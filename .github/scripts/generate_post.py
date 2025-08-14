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

# 文章主题列表
TOPICS = [
    "技术趋势",
    "编程技巧",
    "开发工具",
    "最佳实践",
    "个人成长",
    "技术评测",
    "学习方法",
    "效率提升"
]

def generate_post_topic():
    """生成文章主题和大纲"""
    topic = random.choice(TOPICS)
    prompt = f"""
    请为技术博客生成一篇关于{topic}的文章大纲，要求：
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

def create_post_file(title, content):
    """创建文章文件"""
    now = datetime.now()
    slug = slugify(title)
    filename = f"{now.strftime('%Y-%m-%d')}-{slug}.md"
    
    post = frontmatter.Post(
        content,
        title=title,
        date=now.strftime('%Y-%m-%d'),
        draft=False,
        tags=["AI生成", "技术博客"],
        categories=["技术"],
        author="AI助手",
        featuredImage="",
        toc=True
    )
    
    posts_dir = Path('content/posts')
    posts_dir.mkdir(parents=True, exist_ok=True)
    
    with open(posts_dir / filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

def main():
    # 生成文章主题和大纲
    post_data = generate_post_topic()
    
    # 生成文章内容
    content = generate_post_content(post_data)
    
    # 创建文章文件
    create_post_file(post_data['title'], content)

if __name__ == '__main__':
    main()
