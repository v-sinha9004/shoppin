# 🕷️ Product URL Crawler

A scalable, asynchronous web crawler built using `Playwright`, `aiohttp`, and `BeautifulSoup` to extract product URLs from e-commerce websites that require JavaScript rendering.

---

## 📦 Features

- ✅ Supports both static and JS-rendered pages (via Playwright)
- 🔍 Detects product pages using:
  - URL pattern matching
  - `JSON-LD` structured data
  - `meta` tags like `og:type=product`
  - Keyword-based content scanning
- 💾 Saves discovered URLs to CSV and persists metadata in DB
- 🔁 Automatically crawls internal links with controlled depth
- 🧠 Domain-specific crawling behavior using a JSON config

---

## 🛠️ Tech Stack

- **Python 3.8+**
- `aiohttp` — Async HTTP requests
- `Playwright` — Headless browser automation
- `BeautifulSoup` — HTML parsing
- `CSV`, `JSON`, `os`, `re` — Core utilities
- `asyncio` — Concurrency
- `pymongo` - Database

---

### 📦 Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

## 📁 Project Structure

```
ProductCrawler/
├── config/
│   └── domains.json           # Domain-specific settings
├── output/                    # CSVs for crawled results
├── utils/
│   ├── constants.py           # Static values and keywords
│   ├── config_loader.py       # Load & access domain config
│   ├── helpers.py             # Link extraction, product detection, etc.
│   └── playwright_fetcher.py  # JS rendering using Playwright
├── db.py                      # Function to persist scraped data
├── main.py                    # Entry point
└── README.md                  # This file
```

---

## ⚙️ Config File: `config/domains.json`

Define each domain’s behavior:

```json
{
  "westside.com": {
    "requires_js": true,
    "product_url_patterns": ["/product/"]
  },
  "nykaafashion.com": {
    "requires_js": true,
    "product_url_patterns": ["/p/", "/product/"]
  }
}
```

---

## ▶️ Usage

```bash
python main.py
```

This will crawl each domain in `config/domains.json`, find product URLs, and save them in:

```
output/<domain>.csv
```

Each row contains:

```
[reason_matched, product_url]
```

Example:

```
JSON-LD @type: Product, https://www.example.com/product/shoes123
```

---

## 💾 Saving to DB

`db.py` provides a `save_scraped_data(url, domain_key, is_product, reason)` function.

You can integrate this with your own DB system (e.g., PostgreSQL, MySQL, MongoDB).

---

## 🛠️ Production Considerations

To scale and run this crawler in a production environment, keep in mind:

### ✅ Headless Environment Setup

- Install **screen** or **tmux** so you can run long crawling jobs persistently:
  ```bash
  sudo apt install screen
  screen -S crawler-session
  ```
  Then inside screen:
  ```bash
  python main.py
  ```
  Detach: `Ctrl+A D`, Reattach later: `screen -r crawler-session`

### ✅ Storage & Search

When data grows to **millions of records**, consider:

- Use **Elasticsearch** to store and search through product URLs efficiently.
- Replace `save_scraped_data` with a function that indexes into Elasticsearch.

### ✅ Config Management

- Use **external config servers** (e.g., AWS Parameter Store, Vault) in place of hardcoded JSON files.
- Use **environment variables** for things like DB credentials, headless mode toggles, etc.

### ✅ Monitoring & Retry Logic

- Add retry decorators (`tenacity`, custom retry logic) for transient failures.
- Push logs to **Grafana + Loki** or **ELK stack** for real-time monitoring.
- Use queues like **RabbitMQ** or **Kafka** if scaling to multiple workers.

### ✅ Dockerization

- Containerize the app with `Docker` and orchestrate with `Docker Compose` or `Kubernetes`.

### ⚙️ Scaling in Production

- Use Celery with Redis/RabbitMQ to distribute crawling tasks across multiple workers.
- Containerize with Docker and deploy using Kubernetes for horizontal scalability.
- For thousands of domains, use a producer-consumer model with message queues (e.g., Kafka).

---

## 📌 Notes

- Playwright headless mode is automatically disabled for some sites (like Nykaa) to ensure proper rendering.
- Uses multiple product identification techniques for improved accuracy.
- Crawling depth is limited (default: 3) to avoid infinite loops or deep crawling.

---

## 🧑‍💻 Author

**Vishal Sinha**  
Freelance Full Stack Developer | [LinkedIn](https://www.linkedin.com/in/vishal-sinha-dev)

---

## 📝 License

MIT License @ Vishal Sinha
