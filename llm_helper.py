from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import streamlit as st

load_dotenv()

llm = ChatGroq(
    groq_api_key=st.secrets["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile"
)

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in samosa")
    print(response.content)