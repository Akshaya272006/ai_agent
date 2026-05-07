from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


# ==========================================
# CREATE VECTOR DATABASE
# ==========================================

def create_vector_db(df):

    docs = []

    for _, row in df.iterrows():

        text = f"""
        Month: {row['Month']}
        Sales: {row['Sales (INR)']}
        Expenses: {row['Expenses (INR)']}
        Customers: {row['Customers']}
        Inventory Cost: {row['Inventory Cost (INR)']}
        Marketing Spend: {row['Marketing Spend (INR)']}
        Profit: {row['Profit']}
        """

        docs.append(
            Document(page_content=text)
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(
        docs,
        embeddings
    )

    return db