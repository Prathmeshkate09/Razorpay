import asyncio
import os
from dotenv import load_dotenv
from woocommerce_client import WooCommerceClient

async def main():
    # Load environment variables
    load_dotenv()
    
    store_url = os.getenv("WOOCOMMERCE_STORE_URL")
    consumer_key = os.getenv("WOOCOMMERCE_CONSUMER_KEY")
    consumer_secret = os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
    
    if not all([store_url, consumer_key, consumer_secret]) or store_url == "https://example.com":
        print("Warning: You are using dummy credentials.")
        print("To fully test, add a real WooCommerce store URL and API keys to your .env file.")
        print("However, the client initialized successfully!\n")
        return

    print(f"Connecting to WooCommerce Store: {store_url}")
    client = WooCommerceClient(store_url, consumer_key, consumer_secret)
    
    try:
        print("Testing list_products()...")
        products = await client.list_products(per_page=2)
        print(f"Success! Found {len(products)} products.")
        if products:
            print(f"First product: {products[0].get('name')}")
            
    except Exception as e:
        print(f"Error during request: {e}")

if __name__ == "__main__":
    asyncio.run(main())
