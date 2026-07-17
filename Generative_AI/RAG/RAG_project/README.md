# DocuChat AI 📄🤖

DocuChat AI is a lightweight, full-stack Retrieval-Augmented Generation (RAG) web application that allows users to upload custom documents (PDF, DOCX, or TXT) and have interactive, context-aware conversations based entirely on the contents of those files.

This project was intentionally engineered to run within highly constrained server environments (like free-tier hosting), substituting heavy vector databases for an ultra-lightweight, pure Python mathematical search architecture.

## 🚀 Features

- **Multi-Format Document Support:** Seamlessly parses text from PDF, Word (`.docx`), and plain text (`.txt`) documents.
- **Pure Python Similarity Search:** Bypasses heavy storage engines like ChromaDB using a custom-written Cosine Similarity engine to process data inside minimal RAM footprints (< 150MB).
- **Context-Strict Chatting:** Powered by Mistral AI to ensure the assistant only answers questions using the context present in the uploaded document.
- **Modern UI:** Built using a responsive, two-column dynamic layout in Streamlit.
- **Inactivity Protection:** Includes built-in client-side status pings to handle cloud server cold-starts smoothly.

---

## 🏗️ Architecture & Stack

- **Frontend:** Streamlit (UI & Local Session State Management)
- **Backend:** FastAPI (Async API Routing & Lifespan Management)
- **Document Chunking:** LangChain Text Splitters
- **Embeddings Model:** Google Gen AI (`gemini-embedding-001`)
- **LLM Provider:** Mistral AI (`mistral-medium-latest`)

---

## 🛠️ Local Installation & Setup

### Prerequisites
Make sure you have Python 3.10+ installed and possess API keys from both **Mistral AI** and **Google AI Studio**.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
