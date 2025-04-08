import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["product_crawler"]
collection = db["scraped_urls"]

def save_scraped_data(url, domain_key, is_product, reason=None):
    try:
        collection.insert_one({
            "url": url,
            "domain": domain_key,
            "is_product": is_product,
            "reason": reason
        })
    except Exception as e:
        print(f"⚠️ Error saving to MongoDB: {e}")
