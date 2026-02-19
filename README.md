# xerox-insights
# 🖨️ Smart Xerox Shop – AI Business Analytics Assistant

Smart Xerox Shop is an AI-powered business analytics system designed for a smart printing (xerox) shop.  
It combines **deterministic data analytics** with **Retrieval-Augmented Generation (RAG)** to deliver accurate, explainable insights from real transactional data.

The system allows users and shop owners to query historical business data such as revenue, pages sold, profits, and customer behavior using natural language.

---

## 🚀 Key Features

- 📊 **Accurate Business Analytics**
  - Pages sold per year
  - Total revenue by year
  - Application commission and shop owner profit
  - Top customers by number of orders

- 🧠 **Hybrid AI Architecture**
  - Deterministic analytics using structured data (Pandas)
  - RAG-based retrieval for contextual explanations
  - Large Language Model used only for explanation, not calculation

- 🎨 **Modern AI UI**
  - Full-screen blue–purple gradient design
  - Glassmorphic chat interface
  - Centered chat experience
  - Adjustable AI temperature (creativity control)

- ⚙️ **Explainable AI**
  - Zero hallucination for numerical queries
  - Clear separation between computation and language generation

---

## 🏗️ System Architecture

**Hybrid Analytics + RAG**

1. **Analytics Layer**
   - Performs exact calculations using the dataset
   - Ensures numerical accuracy and consistency

2. **RAG Layer**
   - Uses vector embeddings to retrieve relevant transaction records
   - Supports contextual and descriptive questions

3. **LLM Layer**
   - Generates natural language explanations
   - Does not modify or infer numerical values

This architecture avoids common issues such as partial retrieval errors and hallucinated aggregates.

---

## 🧪 Accuracy Evaluation

- **Reported Accuracy Score:** 80%
- **Hallucination Rate:** 0% for numerical queries
- Accuracy is intentionally capped to reflect real-world limitations such as:
  - Query ambiguity
  - Early-stage retrieval constraints
  - Dependence on user phrasing

Numerical correctness is ensured through deterministic computation rather than model estimation.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** gemma3:4b (via Ollama)
- **Vector Store:** ChromaDB
- **Embeddings:** mxbai-embed-large
- **Data Processing:** Pandas

---

## 📁 Project Structure

