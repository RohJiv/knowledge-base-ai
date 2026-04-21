# 🧠 Personal Knowledge Base — RAG AI Chatbot

A production-ready AI application that lets you chat with your own documents using Retrieval-Augmented Generation (RAG). Upload PDFs, Word docs, or text files and ask questions — the AI finds answers from your documents with source citations.

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![LangChain](https://img.shields.io/badge/framework-LangChain-yellow)

---

## 🎯 What It Does

Ever wanted to ask questions about a 500-page PDF without reading it? This tool lets you:

- Upload multiple PDFs, DOCX, or TXT files at once
- Ask questions in plain English — via keyboard OR voice
- Get accurate answers with source citations (which file + page)
- Maintain conversation context across multiple questions
- Remember what was asked earlier in the chat

---

## 💡 Why I Built This

As a Site Reliability Engineer, I often dealt with massive runbooks, incident playbooks, and vendor documentation. Finding the right answer meant searching 200+ page PDFs manually.

I built this to solve that exact problem — a private AI assistant that reads YOUR documents and answers YOUR questions.

This is also the foundation of enterprise AI knowledge bases used by HR, legal, and support teams.

---

## 🏗️ Architecture

```
PDF / DOCX / TXT Files
         ↓
Text Extraction (PyPDF, python-docx)
         ↓
Chunking (2000 chars with 300 overlap)
         ↓
Embeddings (HuggingFace: all-MiniLM-L6-v2)
         ↓
Vector Storage (ChromaDB)
         ↓
Semantic Search (top-k retrieval)
         ↓
LLM Response Generation (OpenAI-compatible)
         ↓
Streamlit Chat UI with Voice Input
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📚 Multi-file Support | Upload PDF, DOCX, TXT together |
| 🔍 Source Citations | See which file and page answered your question |
| 🎤 Voice Input | Speak your question instead of typing |
| 🧠 Conversation Memory | AI remembers previous questions |
| 🔎 Deep Search Mode | Detects detailed questions, fetches more context |
| 🎨 Streaming Responses | Word-by-word streaming like ChatGPT |
| 🔄 Reset & Reload | Upload new documents anytime |

---

## 🛠️ Tech Stack

- **Framework:** LangChain
- **LLM:** OpenAI GPT-4 compatible APIs
- **Embeddings:** HuggingFace Sentence Transformers
- **Vector DB:** ChromaDB
- **UI:** Streamlit
- **Voice:** SpeechRecognition
- **Document Parsing:** PyPDF, python-docx

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/RohJiv/knowledge-base-ai.git
cd knowledge-base-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# OPENAI_API_KEY=your_key_here

# Run
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📖 How RAG Works (Simple Explanation)

**RAG = Retrieval-Augmented Generation**

Instead of asking an LLM to remember your documents (it can't), we:

1. **Break** your PDFs into small chunks
2. **Convert** each chunk to numbers (embeddings)
3. **Store** them in a searchable database
4. When you ask a question → **find** the most similar chunks
5. **Send** those chunks + your question to the LLM
6. LLM generates answer based on YOUR documents

This is how ChatGPT plugins, Notion AI, and enterprise knowledge bots work under the hood.

---

## 🎓 What I Learned Building This

- RAG pipeline design and tuning (chunk size, overlap, k value)
- Embedding models and similarity search
- Vector database operations with ChromaDB
- Prompt engineering for document Q&A
- Streaming responses and async LLM calls
- Building conversational memory for multi-turn chats
- Streamlit session state management

---

## 🔐 Security Notes

- API keys stored in `.env` (excluded from git)
- Documents processed locally — never sent to third-party storage
- ChromaDB runs in-memory during sessions
- No personal data is logged or retained

---

## 👤 Author

**Phani Rajiv G**
Technical Program Manager | Cloud & AI Platforms
📍 Hyderabad, India
📧 phani.rg@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/phanirajivg)

---

## 📄 License

MIT License — feel free to use this code for learning purposes.

---

⭐ If you found this useful, consider giving it a star!
