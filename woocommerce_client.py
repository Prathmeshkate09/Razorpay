import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

class RateLimitError(Exception):
    pass

class WooCommerceClient:
    """
    Client for interacting with the WooCommerce REST API.
    Handles authentication and rate limiting with exponential backoff.
    """
    def __init__(self, store_url: str, consumer_key: str, consumer_secret: str):
        self.store_url = store_url.rstrip('/')
        # WooCommerce supports Basic Auth over HTTPS with Consumer Key and Secret
        self.auth = (consumer_key, consumer_secret)
        self.base_url = f"{self.store_url}/wp-json/wc/v3"
        self.client = httpx.AsyncClient(auth=self.auth, base_url=self.base_url, timeout=10.0)

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((RateLimitError, httpx.RequestError))
    )
    async def _request(self, method: str, endpoint: str, params: dict = None, json: dict = None) -> dict:
        """
        Internal request method with exponential backoff for rate limiting and network errors.
        """
        response = await self.client.request(method, endpoint, params=params, json=json)
        
        # WooCommerce might return 429 Too Many Requests if rate limits are hit
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
            
        response.raise_for_status()
        return response.json()

    async def list_orders(self, page: int = 1, per_page: int = 10) -> list:
        """Fetch a list of recent orders."""
        return await self._request("GET", "/orders", params={"page": page, "per_page": per_page})
        
    async def get_order(self, order_id: int) -> dict:
        """Fetch a specific order by ID."""
        return await self._request("GET", f"/orders/{order_id}")
        
    async def search_orders(self, search_query: str) -> list:
        """Search for orders based on a string (like customer email)."""
        return await self._request("GET", "/orders", params={"search": search_query})
        
    async def list_products(self, page: int = 1, per_page: int = 10) -> list:
        """Fetch a list of products."""
        return await self._request("GET", "/products", params={"page": page, "per_page": per_page})

    async def get_product(self, product_id: int) -> dict:
        """Fetch a specific product by ID."""
        return await self._request("GET", f"/products/{product_id}")

    async def search_products(self, search_query: str) -> list:
        """Search for products based on a string (like product name or SKU)."""
        return await self._request("GET", "/products", params={"search": search_query})
