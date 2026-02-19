import streamlit as st
import re
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from analytics import (
    pages_sold_by_year,
    revenue_by_year,
    app_profit_by_year,
    shop_profit_by_year,
    top_users_by_orders
)
from vector import retriever

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Xerox Shop",
    page_icon="🖨️",
    layout="wide"
)

# ---------------- FINAL UI CSS ----------------
st.markdown(
    """
    <style>
    /* Remove default Streamlit spacing */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Full app background */
    .stApp {
        background: linear-gradient(135deg, #0b132b, #1c2541, #3a506b, #5bc0be);
        color: white;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.88);
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Hero section */
    .hero {
        padding: 90px 20px 40px 20px;
        text-align: center;
    }

    .hero h1 {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }

    .hero h3 {
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 6px;
    }

    .hero p {
        opacity: 0.75;
        font-size: 1.05rem;
    }

    /* Centered chat container */
    .chat-wrapper {
        display: flex;
        justify-content: center;
        padding: 30px 0 40px 0;
    }

    .chat-box {
        width: 100%;
        max-width: 880px;
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(18px);
        border-radius: 22px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* Chat bubbles */
    .chat-card {
        background: rgba(255,255,255,0.14);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 16px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.14);
    }

    /* ===== FIX STREAMLIT CHAT INPUT BLACK BAR ===== */
    div[data-testid="stChatInput"] {
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] > div {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,0.18) !important;
        backdrop-filter: blur(14px);
        border-radius: 18px !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        color: white !important;
        padding: 14px 16px !important;
    }

    div[data-testid="stChatInput"] button {
        background: rgba(255,255,255,0.25) !important;
        border-radius: 50% !important;
        border: none !important;
    }

    /* Kill bottom spacer background */
    div[data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HERO ----------------
st.markdown(
    """
    <div class="hero">
        <h1>🖨️ Smart Xerox Shop</h1>
        <h3>AI-Powered Business Analytics Assistant</h3>
        <p>
            Intelligent insights on revenue, pages sold, profits, and customer behavior.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## ⚙️ AI Settings")
st.sidebar.caption("Control how expressive the AI responses are")

temperature = st.sidebar.slider(
    "AI Temperature",
    0.0, 1.0, 0.3, 0.05
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Project:** Smart Xerox Shop  
    **Model:** gemma3:4b  
    **Architecture:** Hybrid Analytics + RAG  
    """
)

# ---------------- LLM ----------------
@st.cache_resource
def load_llm(temp):
    return OllamaLLM(model="gemma3:4b", temperature=temp)

llm = load_llm(temperature)

explain_prompt = ChatPromptTemplate.from_template(
    """
You are a professional business analytics assistant.
Explain the result clearly and professionally.

Result:
{result}
"""
)

# ---------------- CHAT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='chat-wrapper'><div class='chat-box'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(
            f"<div class='chat-card'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# ---------------- HELPERS ----------------
def extract_year(text):
    match = re.search(r"(2023|2024|2025)", text)
    return int(match.group()) if match else None

# ---------------- USER INPUT ----------------
if question := st.chat_input("Ask something like: What is the revenue of 2025?"):

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Smart Xerox data..."):

            q = question.lower()
            year = extract_year(q)

            if year and any(k in q for k in ["page", "revenue", "profit", "earning"]):

                if "page" in q:
                    result = f"Total pages sold in {year}: {pages_sold_by_year(year)}"
                elif "app" in q:
                    result = f"Application profit in {year}: ₹{app_profit_by_year(year):.2f}"
                elif "shop" in q:
                    result = f"Shop owner profit in {year}: ₹{shop_profit_by_year(year):.2f}"
                else:
                    result = f"Total revenue in {year}: ₹{revenue_by_year(year):.2f}"

                response = llm.invoke(explain_prompt.format(result=result))

            elif "highest number of orders" in q or "most orders" in q:
                top_users = top_users_by_orders()
                response = llm.invoke(
                    explain_prompt.format(
                        result="Users with the highest number of orders:\n" +
                        "\n".join(f"{u}: {c} orders" for u, c in top_users.items())
                    )
                )
            else:
                records = retriever.invoke(question)
                response = llm.invoke(
                    f"Answer using only these records:\n{records}\n\nQuestion: {question}"
                )

            st.markdown(
                f"<div class='chat-card'>{response}</div>",
                unsafe_allow_html=True
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

st.markdown("</div></div>", unsafe_allow_html=True)
