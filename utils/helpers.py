from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os
import csv
import json
import re
from .constants import OUTPUT_DIR, PRODUCT_PAGE_KEYWORDS
from .playwright_fetcher import fetch_with_playwright
from db import save_scraped_data

def normalize_domain(url):
    return urlparse(url).netloc.replace("www.", "")

def extract_links(base_url, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for tag in soup.find_all('a', href=True):
            href = urljoin(base_url, tag['href'])
            if urlparse(href).netloc == urlparse(base_url).netloc:
                links.add(href.split('#')[0])
        return links
    except Exception as e:
        print(f"⚠️ Error extracting links: {e}")
        return set()

def is_product_url(url, domain, html=None):
    from .config_loader import load_domain_config
    DOMAIN_CONFIG = load_domain_config()
    try:
        domain_key = normalize_domain(domain)
        patterns = DOMAIN_CONFIG.get(domain_key, {}).get("product_url_patterns", [])

        for p in patterns:
            if p in url:
                return True, f"matched pattern: {p}"

        if html:
            soup = BeautifulSoup(html, 'html.parser')
            json_ld = soup.find('script', type='application/ld+json')
            if json_ld:
                try:
                    data = json.loads(json_ld.string)
                    if isinstance(data, dict) and data.get("@type") == "Product":
                        return True, "JSON-LD @type: Product"
                except:
                    pass
            if soup.find('meta', attrs={"property": "og:type", "content": "product"}):
                return True, "meta og:type=product"

            page_text = soup.get_text().lower()
            for keyword in PRODUCT_PAGE_KEYWORDS:
                if " " in keyword:
                    if keyword in page_text:
                        return True, keyword
                else:
                    if re.search(rf'\b{re.escape(keyword)}\b', page_text):
                        return True, keyword
        return False, "no match"
    except Exception as e:
        print(f"⚠️ Error checking product URL: {e}")
        return False, "exception"

def save_to_csv(domain_key, url, reason, is_product):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        csv_path = os.path.join(OUTPUT_DIR, f"{domain_key}.csv")
        seen_urls = set()

        if os.path.exists(csv_path):
            with open(csv_path, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        seen_urls.add(row[1])

        if url not in seen_urls:
            with open(csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([reason, url])

            save_scraped_data(url, domain_key, is_product, reason if is_product else None)
    except Exception as e:
        print(f"⚠️ Error saving to CSV: {e}")

async def fetch(session, url, use_playwright=False):
    if use_playwright:
        return await fetch_with_playwright(url)
    try:
        async with session.get(url, timeout=10) as response:
            if 'text/html' in response.headers.get('Content-Type', ''):
                return await response.text()
    except Exception as e:
        print(f"⚠️ Fetch error: {e}")
        return None
