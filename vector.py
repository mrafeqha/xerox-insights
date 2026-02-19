import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

CSV_FILE = r"C:\Users\fahee\Downloads\Smart_Xerox_3000_Orders_2023_2025.csv"

DB_LOCATION = "./chroma_xerox_db"
COLLECTION_NAME = "smart_xerox_orders"

df = pd.read_csv(CSV_FILE)

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings
)

# Ingest only once
if vector_store._collection.count() == 0:
    documents = []

    for _, row in df.iterrows():
        text = (
            f"On {row['Date']}, order {row['Order_ID']} was completed. "
            f"The user printed {row['Total_Pages_Printed']} pages. "
            f"Total amount paid was ₹{row['Total_Amount']}. "
            f"Shop earned ₹{row['Shop_Earning']} and "
            f"app earned ₹{row['App_Earning']}."
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "date": row["Date"],
                    "order_id": row["Order_ID"],
                    "user": row["User_Name"]
                }
            )
        )

    vector_store.add_documents(documents)

retriever = vector_store.as_retriever(search_kwargs={"k": 20})
