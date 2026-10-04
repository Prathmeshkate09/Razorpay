import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from woocommerce_client import WooCommerceClient

# Load environment variables from .env file
load_dotenv()

# Initialize WooCommerce Client
store_url = os.getenv("WOOCOMMERCE_STORE_URL")
consumer_key = os.getenv("WOOCOMMERCE_CONSUMER_KEY")
consumer_secret = os.getenv("WOOCOMMERCE_CONSUMER_SECRET")

if not all([store_url, consumer_key, consumer_secret]):
    raise ValueError("Missing WooCommerce configuration in environment variables. Please check your .env file.")

wc_client = WooCommerceClient(store_url, consumer_key, consumer_secret)

# Initialize FastMCP Server
mcp = FastMCP("woocommerce-connector")

@mcp.tool()
async def list_orders(page: int = 1, per_page: int = 10) -> str:
    """
    List recent orders from WooCommerce.
    
    Args:
        page: Page number (default 1).
        per_page: Number of items per page (default 10).
    """
    data = await wc_client.list_orders(page, per_page)
    return str(data)

@mcp.tool()
async def get_order(order_id: int) -> str:
    """
    Get a specific order by its ID.
    
    Args:
        order_id: The unique ID of the order in WooCommerce.
    """
    data = await wc_client.get_order(order_id)
    return str(data)

@mcp.tool()
async def search_orders(search_query: str) -> str:
    """
    Search for orders using a search term.
    
    Args:
        search_query: The email address, customer name, or order details to search for.
    """
    data = await wc_client.search_orders(search_query)
    return str(data)

@mcp.tool()
async def list_products(page: int = 1, per_page: int = 10) -> str:
    """
    List products from the WooCommerce store.
    
    Args:
        page: Page number (default 1).
        per_page: Number of items per page (default 10).
    """
    data = await wc_client.list_products(page, per_page)
    return str(data)

@mcp.tool()
async def get_product(product_id: int) -> str:
    """
    Get a specific product by its ID.
    
    Args:
        product_id: The unique ID of the product.
    """
    data = await wc_client.get_product(product_id)
    return str(data)

@mcp.tool()
async def search_products(search_query: str) -> str:
    """
    Search for products by name or SKU.
    
    Args:
        search_query: The product name or SKU to search for.
    """
    data = await wc_client.search_products(search_query)
    return str(data)

if __name__ == "__main__":
    # Start the MCP stdio server
    mcp.run()
