# 导入所需库
import requests  # 用于发送HTTP请求
from bs4 import BeautifulSoup  # 用于解析HTML
import json  # 用于处理数据（可选）

# 需要用户自行添加的请求头（将在代码中用注释指导获取）
# 1. 打开Chrome浏览器
# 2. 访问 https://ai-bot.cn/daily-ai-news/
# 3. 按F12打开开发者工具
# 4. 选择Network选项卡
# 5. 刷新页面
# 6. 找到一个请求，例如daily-ai-news/
# 7. 在Headers选项卡中找到User-Agent，复制它的值并粘贴到下面
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

# 定义目标网址
url = "https://ai-bot.cn/daily-ai-news/"

# 发送GET请求
response = requests.get(url, headers=headers)

# 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 查找新闻条目（需要根据实际网页结构调整选择器）
# 经过分析，发现每个新闻条目的class是 media
news_items = soup.select('.media')

print(f"Number of news items found: {len(news_items)}")
print(soup.prettify())

# 将内容写入txt文件
with open('ai_news.txt', 'w', encoding='utf-8') as f:
    for item in news_items:
        # 提取标题和链接
        title_element = item.select_one('.media-heading a')
        if title_element:
            title = title_element.text.strip()
            link = item.select_one('.media-heading a')['href']
            f.write(f"{title}\n{link}\n\n")
        else:
            print("title_element is None")
