# app.py — Personal Knowledge Base (Clean Fixed Version)

import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# ── Load API key ──────────────────────────────────────────────
load_dotenv()

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="🧠 My Knowledge Base",
    page_icon="🧠",
    layout="wide"
)

# ── Initialize ALL session state at the top ───────────────────
# This must happen before ANYTHING else
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None

if "pdfs_processed" not in st.session_state:
    st.session_state["pdfs_processed"] = False

# ── Title ─────────────────────────────────────────────────────
st.title("🧠 Personal Knowledge Base")
st.caption("Upload your PDFs and chat with them like your own AI brain")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("📎 Upload Your PDFs")

    uploaded_files = st.file_uploader(
        "Drag and drop PDFs here",
        type="pdf",
        accept_multiple_files=True
    )

    # Show uploaded file names
    if uploaded_files:
        for f in uploaded_files:
            st.write(f"📄 {f.name}")

    st.divider()

    # Show Process button ONLY if not yet processed
    if not st.session_state["pdfs_processed"]:
        process_btn = st.button("🚀 Process PDFs", type="primary")
    else:
        process_btn = False
        st.success("✅ PDFs are ready!")
        # Reset button only shows AFTER processing is done
        if st.button("🔄 Reset — Upload New PDFs"):
            st.session_state["chat_history"] = []
            st.session_state["messages"] = []
            st.session_state["vectorstore"] = None
            st.session_state["pdfs_processed"] = False
            st.rerun()

    st.divider()
    st.caption("Built by Sahaji | Powered by Groq + LangChain")

# ── Process PDFs ──────────────────────────────────────────────
if process_btn and uploaded_files and not st.session_state["pdfs_processed"]:

    all_chunks = []

    with st.spinner("📄 Reading your PDFs..."):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=300
            )
            chunks = splitter.split_documents(documents)
            all_chunks.extend(chunks)
            os.unlink(tmp_path)

    with st.spinner(f"🧮 Creating embeddings for {len(all_chunks)} chunks..."):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(
            documents=all_chunks,
            embedding=embeddings
        )
        # Save to session state
        st.session_state["vectorstore"] = vectorstore
        st.session_state["pdfs_processed"] = True

    st.rerun()  # ← rerun ONCE after processing to refresh the UI

# ── Block chat until PDFs are processed ──────────────────────
if not st.session_state["pdfs_processed"]:
    st.info("👈 Upload your PDFs in the sidebar and click 'Process PDFs' to begin")
    st.stop()

# ── Display existing chat history ────────────────────────────
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



# ── Chat input ────────────────────────────────────────────────
question = st.chat_input("Ask anything about your documents...")

if question:

    # Show user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state["chat_history"].append({
        "role": "user",
        "content": question
    })

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching documents..."):

            # Deep search for detailed questions
            detail_keywords = ["detail", "full", "complete", "everything",
                              "all", "entire", "explain", "elaborate", "tell me about"]
            wants_detail = any(w in question.lower() for w in detail_keywords)
            k = 15 if wants_detail else 10

            # Retrieve chunks
            docs = st.session_state["vectorstore"].similarity_search(question, k=k)
            context = "\n\n".join(doc.page_content for doc in docs)

            # LLM
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=get_api_key()
            )

            # Prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a thorough document assistant.

STRICT RULES:
- Answer using ONLY the context provided
- For detailed questions reproduce every relevant line
- Never say cannot find unless truly absent
- Format long answers with headings and bullet points
- Be thorough and complete

Context from documents:
{context}
"""),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}")
            ])

            chain = prompt | llm | StrOutputParser()

            # Stream response word by word
            response = st.write_stream(
                chain.stream({
                    "context": context,
                    "chat_history": st.session_state["messages"],
                    "question": question
                })
            )

    # Save to histories
    st.session_state["chat_history"].append({
        "role": "assistant",
        "content": response
    })
    st.session_state["messages"].append(HumanMessage(content=question))
    st.session_state["messages"].append(AIMessage(content=response))
"""```

---

## 🧠 What Was Wrong and What's Fixed

| Problem | Root Cause | Fix |
|---|---|---|
| Processing again and again | `pdfs_processed` check was inconsistent | Unified all checks using `st.session_state["pdfs_processed"]` with quotes everywhere |
| Reset button not visible | Button was outside the correct sidebar block | Moved inside `with st.sidebar` and only shows AFTER processing |
| Process button showing after done | No condition hiding it | Process button now ONLY shows when `pdfs_processed = False` |

---

Save (`Ctrl+S`) and run:
```
streamlit run app.py
"""