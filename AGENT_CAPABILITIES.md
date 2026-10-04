# Agent Capabilities

This document outlines the specific capabilities of the WooCommerce Connector agent, establishing clear boundaries of what it **can** and **cannot** do when connected to a merchant's store.

### What the Agent CAN Do
The agent is empowered to securely fetch and analyze read-only data from the store:

- **List Recent Orders**: The agent can retrieve a chronological list of recent orders, fetching their statuses, totals, and timestamps. It can paginate through history if asked to summarize recent activity.
- **Retrieve Specific Order Details**: The agent can fetch all details for a given `order_id`, allowing it to answer customer queries regarding line items, shipping addresses, tracking numbers (if stored in metadata), and tax breakdowns.
- **Search Orders**: The agent can search the entire order history using a specific customer email, name, or keyword, making it highly effective at resolving "Where is my order?" inquiries automatically.
- **List & Search Products**: The agent can look up the current catalog, including stock availability, pricing, and descriptions using either pagination or specific search terms (like SKU or product name).

### What the Agent CANNOT Do
To ensure absolute safety and prevent "rogue" actions in production, strict guardrails have been applied at the connector level:

- **Cannot Create or Modify Orders**: The agent is structurally incapable of changing order statuses, issuing refunds, or creating manual orders. Any request to do so will be ignored by the connector.
- **Cannot Change Prices or Inventory**: The agent cannot update product pricing, modify stock levels, or delete products from the catalog.
- **Cannot Bypass Rate Limits**: The agent cannot flood the merchant's server. All operations are strictly rate-limited through an exponential backoff wrapper.
- **Cannot Access Non-WooCommerce Data**: The agent can only read data exposed by the standard `/wp-json/wc/v3/orders` and `/wp-json/wc/v3/products` endpoints. It cannot read raw WordPress data, merchant passwords, or plugin settings.
