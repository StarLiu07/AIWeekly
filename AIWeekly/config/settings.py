# -*- coding: utf-8 -*-

# 爬虫配置
BASE_URL = "https://ai-bot.cn/daily-ai-news/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/123.0.0.0 Safari/537.36'
}
REQUEST_INTERVAL = 2  # 请求间隔(秒)
TIMEOUT = 10  # 超时时间

# 数据存储
DATA_DIR = "../data"
CSV_FILENAME = "daily_ai_news.csv"

# PDF输出
PDF_DIR = "../reports"
PDF_TEMPLATE = "weekly_report_template.pdf"
LOGO_PATH = "logo.png"

# 系统日志
LOG_FILE = "../logs/crawler.log"
