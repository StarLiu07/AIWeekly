import requests
import time
import os

def scrape_website(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Successfully scraped {url} and saved to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return False
    return True

if __name__ == "__main__":
    url = "https://ai-bot.cn/daily-ai-news/"
    output_file = "sources.txt"
    if scrape_website(url, output_file):
        print("Scraping completed successfully.")
    else:
        print("Scraping failed.")
