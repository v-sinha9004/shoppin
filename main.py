# main.py
import asyncio
from utils.helpers import normalize_domain, extract_links, is_product_url, save_to_csv, fetch
from utils.constants import CONFIG_PATH
from utils.config_loader import load_domain_config, get_domain_config

DOMAIN_CONFIG = load_domain_config()

async def crawl_domain(domain_url, visited, domain_key, max_depth=3):
    try:
        print(f"Crawling {domain_url}...")
        start_url = domain_url if domain_url.endswith('/') else domain_url + '/'
        queue = [(start_url, 0)]

        headers = {"User-Agent": "Mozilla/5.0 (compatible; ProductCrawler/1.0)"}
        config = get_domain_config(domain_key, DOMAIN_CONFIG)
        requires_js = config.get("requires_js", False)

        import aiohttp
        async with aiohttp.ClientSession(headers=headers) as session:
            while queue:
                try:
                    current_url, depth = queue.pop(0)
                    if current_url in visited or depth > max_depth:
                        continue
                    visited.add(current_url)

                    html = await fetch(session, current_url, use_playwright=requires_js)
                    if not html:
                        continue

                    is_product, reason = is_product_url(current_url, domain_key, html)
                    save_to_csv(domain_key, current_url, reason, is_product)

                    if not is_product:
                        links = extract_links(current_url, html)
                        for link in links:
                            if link not in visited:
                                queue.append((link, depth + 1))
                except Exception as e:
                    print(f"⚠️ Error crawling URL: {e}")
                    continue
    except Exception as e:
        print(f"⚠️ Error in crawl_domain: {e}")

async def main():
    try:
        from utils.config_loader import load_domain_config
        domains_config = load_domain_config()
        domains = list(domains_config.keys())

        tasks = []
        for domain in domains:
            visited = set()
            domain_key = normalize_domain(domain)
            tasks.append(crawl_domain(domain, visited, domain_key))

        await asyncio.gather(*tasks)
        print("Crawling complete. Product URLs saved in individual domain CSVs under ./output/")
    except Exception as e:
        print(f"⚠️ Error in main: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"⚠️ Uncaught exception: {e}")
