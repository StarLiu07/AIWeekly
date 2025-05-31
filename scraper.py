import os
import datetime
import re
import json
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp

# Initialize Firecrawl with the provided API key
api_key = "fc-99aacd9b6cc342bba3c22c5fe6102e2a"
app = FirecrawlApp(api_key=api_key)

def parse_news_date(date_str, current_year):
    # print(f"Debug - raw date string: {date_str}")
    
    match = re.match(r"(\d{1,2}月\d{1,2}日)", date_str)
    if not match:
        match = re.match(r"(\d{1,2}月\d{1,2})", date_str)
        if not match:
        # print(f"Could not parse date format: {date_str}")
            return None
        date_part = match.group(1) + "日"
    else:
        date_part = match.group(1)
    
    try:
        date_obj = datetime.datetime.strptime(f"{current_year}年{date_part}", "%Y年%m月%d日").date()
        return date_obj.isoformat()
    except ValueError:
        print(f"Error parsing date string: {date_str}")
        return None

def scrape_website(url, output_file):
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    
    try:
        # Use Firecrawl to scrape the URL
        data = app.scrape_url(url, formats=['html'])
        
        if not data or not data.html:
            print("Firecrawl scrape failed or no HTML content returned.")
            print(f"Firecrawl response: {data}") # Added debug print
            return False

        # print("Debug - Firecrawl returned HTML, proceeding to parse.") # New debug print

        # Parse HTML content from Firecrawl
        soup = BeautifulSoup(data.html, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')

        # print(f"Debug - Found {len(news_items)} news items.") # Added debug print

        seven_days_ago = (today - datetime.timedelta(days=7)).isoformat()
        news_data = []

        for item in news_items:
            date_str_zh = item.find_previous_sibling('div', class_='news-date').get_text(strip=True)
            # print(f"Debug - Processing date string: {date_str_zh}") # Added debug print
            parsed_month = int(date_str_zh.split('月')[0])
            year = current_year - 1 if parsed_month > current_month else current_year
            news_date_iso = parse_news_date(date_str_zh, year)

            # print(f"Debug - Parsed date ISO: {news_date_iso}, Seven days ago: {seven_days_ago}") # Added debug print

            # print(f"Debug - Comparing news_date_iso ({news_date_iso}) with seven_days_ago ({seven_days_ago})") # Added debug print
            if news_date_iso is None or news_date_iso < seven_days_ago:
                # print(f"Debug - Skipping item with date: {news_date_iso}") # Added debug print
                continue

            title = item.find('h2').get_text(strip=True)
            desc = item.find('p', class_='text-muted').get_text(strip=True)

            news_item_data = {
                "date_zh": date_str_zh,
                "date_iso": news_date_iso,
                "title": title,
                "description": desc
            }
            news_data.append(news_item_data)

        now = datetime.datetime.now()
        output_data = {
            "scrape_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "news_count": len(news_data),
            "news_items": news_data
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print(f"Successfully extracted {len(news_data)} news items to {output_file}")
        return True

    except Exception as e:
        print(f"Error during scraping: {e}")
        return False

if __name__ == "__main__":
    url = "https://ai-bot.cn/daily-ai-news/"
    output_file = "ai_news.json"
    
    if scrape_website(url, output_file):
        print("Scraping completed successfully.")
    else:
        print("Scraping failed.")
