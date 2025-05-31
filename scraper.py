import requests
from bs4 import BeautifulSoup
import os
import datetime
import re
import json

def parse_news_date(date_str, current_year):
    # Debug print to see actual date string format
    print(f"Debug - raw date string: {date_str}")
    
    # Extract date part like "4月30日" or "5月30·周五"
    match = re.match(r"(\d{1,2}月\d{1,2}日)", date_str)
    if not match:
        # Try alternative format that includes weekday
        match = re.match(r"(\d{1,2}月\d{1,2})", date_str)
        if not match:
            print(f"Could not parse date format: {date_str}")
            return None
        date_part = match.group(1) + "日"  # Add the "日" character
    else:
        date_part = match.group(1)
    try:
        # Combine with current year and parse
        date_obj = datetime.datetime.strptime(f"{current_year}年{date_part}", "%Y年%m月%d日").date()
        return date_obj.isoformat() # Return ISO format string
    except ValueError:
        print(f"Error parsing date string: {date_str}")
        return None

def scrape_website(url, output_file):
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')

        seven_days_ago = (today - datetime.timedelta(days=7)).isoformat() # Compare with ISO format

        news_data = []
        for item in news_items:
            date_str_zh = item.find_previous_sibling('div', class_='news-date').get_text(strip=True)
            # Correct the year if the news date is in the previous year
            parsed_month = int(date_str_zh.split('月')[0])
            year = current_year - 1 if parsed_month > current_month else current_year
            news_date_iso = parse_news_date(date_str_zh, year) # Get ISO date

            # Skip if date parsing failed or date is older than 7 days
            if news_date_iso is None or news_date_iso < seven_days_ago:
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
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        output_data = {
            "scrape_time": timestamp,
            "news_count": len(news_data),
            "news_items": news_data
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print(f"Successfully extracted {len(news_data)} news items from the last 7 days to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return False
    return True

if __name__ == "__main__":
    url = "https://ai-bot.cn/daily-ai-news/"
    output_file = "ai_news.json" # Changed output file extension
    if scrape_website(url, output_file):
        print("Scraping completed successfully.")
    else:
        print("Scraping failed.")
