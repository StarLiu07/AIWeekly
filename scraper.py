import requests
from bs4 import BeautifulSoup
import os

def scrape_website(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')
        
        with open(output_file, "w", encoding="utf-8") as f:
            for item in news_items:
                date = item.find_previous_sibling('div', class_='news-date').get_text(strip=True)
                title = item.find('h2').get_text(strip=True)
                desc = item.find('p', class_='text-muted').get_text(strip=True)
                
                f.write(f"【{date}】\n{title}\n{desc}\n------------------\n")

        print(f"Successfully extracted news to {output_file}")

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
