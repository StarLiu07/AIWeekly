import requests
from bs4 import BeautifulSoup
import os
import datetime
import re

def parse_news_date(date_str, current_year):
    # Extract date part like "4月30日"
    match = re.match(r"(\d{1,2}月\d{1,2}日)", date_str)
    if not match:
        print(f"Could not parse date format: {date_str}")
        return None

    date_part = match.group(1)
    try:
        # Combine with current year and parse
        date_obj = datetime.datetime.strptime(f"{current_year}年{date_part}", "%Y年%m月%d日").date()
        return date_obj
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

        seven_days_ago = today - datetime.timedelta(days=7)

        with open(output_file, "w", encoding="utf-8") as f:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"爬取时间: {timestamp}\n\n")
            news_written_count = 0
            for item in news_items:
                date_str = item.find_previous_sibling('div', class_='news-date').get_text(strip=True)
                # Correct the year if the news date is in the previous year
                parsed_month = int(date_str.split('月')[0])
                year = current_year - 1 if parsed_month > current_month else current_year
                news_date = parse_news_date(date_str, year)

                # Skip if date parsing failed or date is older than 7 days
                if news_date is None or news_date < seven_days_ago:
                    continue

                title = item.find('h2').get_text(strip=True)
                desc = item.find('p', class_='text-muted').get_text(strip=True)

                f.write(f"【{date_str}】\n{title}\n{desc}\n------------------\n")
                news_written_count += 1

        print(f"Successfully extracted {news_written_count} news items from the last 7 days to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return False
    return True

if __name__ == "__main__":
    url = "https://ai-bot.cn/daily-ai-news/"
    output_file = "ai_news.txt"
    if scrape_website(url, output_file):
        print("Scraping completed successfully.")
    else:
        print("Scraping failed.")
