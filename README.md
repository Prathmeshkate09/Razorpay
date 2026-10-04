# Agent Studio - WooCommerce Private Connector

## Overview
This repository contains a production-ready private connector that enables an Agent Studio agent to securely read data from a WooCommerce store. 

This connector is built using the **Model Context Protocol (MCP)**, providing standardized access to WooCommerce primitives such as `List`, `Get`, and `Search` for both **Orders** and **Products**. By wrapping the WooCommerce REST API inside an MCP server, any compatible AI Agent can semantically interact with the merchant's store data safely and deterministically.

## Architecture & Approach
This project leverages **Python** combined with the official `mcp` SDK to construct an asynchronous MCP Server. 
The architectural choices reflect a focus on reliability, which is critical for merchant tools:
- **FastMCP Framework**: Utilizes the modern `FastMCP` standard to natively define tools and their JSON Schema specifications, making it effortless for the LLM to understand expected parameters.
- **Robust Rate-Limiting & Backoff**: Uses the `tenacity` library to wrap all API requests. If WooCommerce returns a `429 Too Many Requests` (or encounters temporary network disruptions), the connector automatically executes exponential backoff logic rather than failing immediately or hallucinating an answer to the agent.
- **Secure Authentication**: Uses API-key authentication (Basic Auth over HTTPS) directly into WooCommerce's `/wp-json/wc/v3` endpoints. All credentials are appropriately isolated in environment variables.

## Setup Instructions

**Prerequisites:**
- Python 3.10+
- A WooCommerce store with REST API enabled. Generate API keys by navigating to `WooCommerce > Settings > Advanced > REST API` in the WordPress dashboard.

**1. Clone the repository and navigate into it**
```bash
git clone <your-repo-link>
cd Razorpay
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Do not commit actual keys. Copy the `.env.example` to create your local configuration:
```bash
cp .env.example .env
```
Edit the `.env` file and insert your actual WooCommerce store URL and keys:
```env
WOOCOMMERCE_STORE_URL="https://your-store.com"
WOOCOMMERCE_CONSUMER_KEY="ck_xxx"
WOOCOMMERCE_CONSUMER_SECRET="cs_xxx"
```

**4. Run the Connector (MCP Server)**
To run the server in standard stdio mode (which the Agent host process connects to):
```bash
python server.py
```
*(Note: Because this operates as an MCP stdio server, you will not see an interactive CLI or Web server start; it awaits JSON-RPC messages via stdin/stdout).*

## Assumptions & Limitations
- **Read-Only Scope**: For safety guardrails, this connector only exposes read operations (`GET` endpoints). Modifications (Create/Update/Delete) are intentionally omitted to prevent accidental data corruption by the Agent during initial iterations.
- **Pagination Assumption**: By default, list and search endpoints return a maximum of 10 items per page unless overridden by the agent. Very large queries are constrained by WooCommerce default parameters.
- **Rate Limits**: The backoff strategy assumes standard WooCommerce REST API limits. If the server is protected by strict WAF (like Cloudflare) that blocks automated traffic, the connector might require specific User-Agent spoofing or whitelist IP bypass which is not implemented here.

## MCP Tool Specification
The MCP `FastMCP` framework automatically generates the JSON schema specifications. Example schema for `search_orders`:
```json
{
  "name": "search_orders",
  "description": "Search for orders using a search term.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "search_query": {
        "type": "string",
        "description": "The email address, customer name, or order details to search for."
      }
    },
    "required": ["search_query"]
  }
}
```
