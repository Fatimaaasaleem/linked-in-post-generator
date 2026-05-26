import streamlit as st
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=st.secrets["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile"
)

if __name__ == "__main__":
    response = llm.invoke(
        "What are the two main ingredients in samosa"
    )

    print(response.content)