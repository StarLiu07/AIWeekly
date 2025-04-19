# -*- coding: utf-8 -*-

# ��������
BASE_URL = "https://ai-bot.cn/daily-ai-news/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/123.0.0.0 Safari/537.36'
}
REQUEST_INTERVAL = 2  # ������(��)
TIMEOUT = 10  # ��ʱʱ��

# ���ݴ洢
DATA_DIR = "../data"
CSV_FILENAME = "daily_ai_news.csv"

# PDF���
PDF_DIR = "../reports"
PDF_TEMPLATE = "weekly_report_template.pdf"
LOGO_PATH = "logo.png"

# ϵͳ��־
LOG_FILE = "../logs/crawler.log"
