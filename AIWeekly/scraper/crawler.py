# -*- coding: utf-8 -*-
import time
import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from config.settings import BASE_URL, HEADERS, REQUEST_INTERVAL, TIMEOUT, DATA_DIR, CSV_FILENAME


class AINewsCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.data_path = f"{DATA_DIR}/{CSV_FILENAME}"
        self.existing_hashes = set()

    def load_existing_data(self):
        """??????????????"""
        try:
            df = pd.read_csv(self.data_path)
            self.existing_hashes = set(df['hash'])
        except FileNotFoundError:
            pass

    def save_data(self, news_items):
        """???????????? CSV ???"""
        df = pd.DataFrame(news_items)
        df.to_csv(self.data_path, mode='a', index=False, header=not hasattr(self, 'header_written'))

        # ??????????
        if not hasattr(self, 'header_written'):
            self.header_written = True

    def fetch_page(self):
        """?? HTTP ????????????? BeautifulSoup ??"""
        response = self.session.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def parse_news(self, soup):
        """??????????"""
        items = []
        for article in soup.select('.article-item'):
            title = article.select_one('.title').get_text(strip=True)
            content = article.select_one('.content').get_text(strip=True)
            link = article.select_one('a')['href']

            # ?????
            item_hash = hashlib.md5((title + content).encode('utf-8')).hexdigest()

            if item_hash not in self.existing_hashes:
                items.append({
                    'title': title,
                    'content': content,
                    'link': link,
                    'hash': item_hash
                })
                self.existing_hashes.add(item_hash)

        return items

    def run(self):
        """??????"""
        self.load_existing_data()
        soup = self.fetch_page()
        news_items = self.parse_news(soup)
        if news_items:
            self.save_data(news_items)
        time.sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    crawler = AINewsCrawler()
    crawler.run()