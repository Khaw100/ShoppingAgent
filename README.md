# 🛍️ Smart Shopping Agent

An AI-powered shopping assistant built with [Google ADK](https://google.github.io/adk-docs/) and MongoDB Atlas Vector Search. The agent can search for products using natural language, filter by brand or material, and handle purchases — all through a conversational interface.

---

## ✨ Features

- 🔍 **Semantic product search** — RAG-powered vector search using `sentence-transformers`
- 🏷️ **Filter by brand or material** — Exact-match queries on product metadata
- 🛒 **Buy items** — Creates a purchase transaction and confirms the order
- 📜 **View transaction history** — Lists all past purchases for the current user
- 🤖 **Powered by Groq LLaMA 3.3 70B** via LiteLLM

---

## 🏗️ Project Structure

```
.
├── main.py                  # Entry point
├── shop_agent/
│   ├── agent.py             # ADK Agent definition & system prompt
│   └── tools.py             # Tool functions exposed to the agent
├── util/
│   ├── mongodb.py           # MongoDB Atlas client & query helpers
│   └── embedding.py         # Sentence-transformer embedding model
├── pyproject.toml
├── requirements.txt
└── .env                     # Environment variables (not committed)
```

---

## ⚙️ Setup

### 1. Clone & install dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv
uv sync
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
db_username=YOUR_MONGODB_USERNAME
db_password=YOUR_MONGODB_PASSWORD
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

### 3. MongoDB Atlas setup

- Create a **MongoDB Atlas** cluster and a database named `rag_db`.
- Create two collections:
  - `rag` — product documents with an `embedding` field (384-dim vectors)
  - `transactions` — stores purchase records
- Create a **Vector Search index** named `vector_index` on the `rag.embedding` field.

### 4. Run the agent

```bash
# Launch in ADK Web UI
adk web

# Or run via CLI
adk run shop_agent
```

---

## 🛠️ Agent Tools

| Tool | Description |
|---|---|
| `search_items` | Vector search over products using a natural language query |
| `search_item_by_id` | Fetch a product by its `product_id` |
| `search_item_by_brand` | Filter products by brand name |
| `search_item_by_material` | Filter products by material (case-insensitive) |
| `buy_item` | Purchase a product and log the transaction |
| `get_my_transactions` | Retrieve the current user's purchase history |

---

## 🧠 How It Works

```
User message
     │
     ▼
 ADK Agent (LLaMA 3.3 70B via Groq)
     │
     ├── search_items()  ──►  Embedding (MiniLM-L6-v2)  ──►  MongoDB $vectorSearch
     ├── search_item_by_brand() / search_item_by_material()  ──►  MongoDB find()
     ├── buy_item()  ──►  create_transaction()  ──►  MongoDB insert
     └── get_my_transactions()  ──►  MongoDB find() + sort
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `google-adk` | Agent framework |
| `litellm` | LLM provider abstraction (Groq) |
| `pymongo[srv]` | MongoDB Atlas client |
| `sentence-transformers` | Local embedding model |
| `python-dotenv` | Environment variable loading |

---

## 📄 License

MIT
