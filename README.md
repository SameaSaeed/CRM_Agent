# 🤖 CRM Agent for targeted marketing

Welcome to the **CRM Agent**!; an intelligent Customer Relationship Management (CRM) system using AI agents, LangGraph, and real customer data. Meet an AI-powered marketing assistant who can analyze customer behavior, create personalized marketing campaigns, and automate email communications.

## 🎯 Deliverables

- AI agent using **LangGraph** and **ChatGroq**
- **human-in-the-loop** workflows for sensitive operations
- **RFM (Recency, Frequency, Monetary) analysis** for customer segmentation
- **personalized marketing campaigns** using AI
- **PostgreSQL** with AI agents for real-time data analysis
- **Model Context Protocol (MCP)** for tool integration
- **Docker** for containerization

## 🏗️ Project Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Ralph Agent   │    │   Database      │
│   (Chat UI)     │◄──►│   (LangGraph)   │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  MCP Marketing  │
                       │     Server      │
                       └─────────────────┘
```

## 🚀 Features

- **🧠 Intelligent Customer Analysis**: Ralph analyzes customer purchase history and behavior patterns
- **📧 Personalized Email Campaigns**: Creates targeted marketing emails with customer-specific content
- **🎯 Customer Segmentation**: Uses RFM analysis to categorize customers (Champions, At Risk, etc.)
- **✋ Human Approval**: Requires human review for sensitive actions like sending campaigns
- **📊 Real-time Data**: Works with actual retail transaction data
- **🔄 Campaign Types**:
  - **Re-engagement**: Win back inactive customers
  - **Referral**: Leverage high-value customers for referrals
  - **Loyalty**: Thank and retain valuable customers

## 📋 Prerequisites

- **Python 3.13+** installed
- **PostgreSQL** database (we'll use Supabase)
- **ChatGroq API key**
- **Git** for cloning the repository

## ⚡ Quick Start

Want to get started immediately? Here's the fastest path:

This project uses `uv` for dependency management. If you don't have `uv` installed, follow the instructions [here](https://docs.astral.sh/uv/guides/install-python/).

   ```bash
   git clone https://github.com/SameaSaeed/CRM_Agent
   cd crm-agent
   docker-compose up --build
   ```

## 🎯 Example Output

<img width="850" height="448" alt="output2" src="https://github.com/user-attachments/assets/3d664e55-5f3f-4d23-8b1b-34471e30e21e" />

<img width="854" height="434" alt="output3" src="https://github.com/user-attachments/assets/0d58a980-1d28-4fc7-9ca3-6040acb148a7" />


### Example Interactions

Try these commands to see Ralph in action:

1. **Customer Analysis**:
   ```
   "Show me our top 5 customers by total spending"
   ```

2. **Segment Analysis**:
   ```
   "How many customers do we have in each RFM segment?"
   ```

3. **Create a Campaign**:
   ```
   "Create a re-engagement campaign for customers who haven't purchased in the last 6 months"
   ```

4. **Send Personalized Emails**:
   ```
   "Send a loyalty email to our champion customers thanking them for their business"
   ```

## 📊 Understanding the Data

### Customer Segments (RFM Analysis)

Ralph uses RFM analysis to categorize customers:

- **🏆 Champions** (555): Best customers - high recency, frequency, and monetary value
- **🆕 Recent Customers** (5XX): Recently active customers
- **🔄 Frequent Buyers** (X5X): Customers who buy often
- **💰 Big Spenders** (XX5): High-value customers
- **⚠️ At Risk** (1XX): Haven't purchased recently
- **👥 Others**: Everyone else

### Database Schema

The project includes these main tables:

- **customers**: Customer information and contact details
- **transactions**: Purchase history and transaction data
- **items**: Product catalog with descriptions and prices
- **rfm**: Customer segmentation scores
- **marketing_campaigns**: Campaign tracking
- **campaign_emails**: Email delivery and engagement tracking

## Adding New Tools

Create new MCP tools in `src/ralph/mymcp/servers/marketing_server.py`:

```python
@mcp.tool()
async def your_new_tool(param: str) -> str:
    """Your tool description."""
    # Your implementation here
    return "Tool result"
```

