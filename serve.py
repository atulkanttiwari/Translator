from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key = None
try:
    import streamlit as st

    groq_api_key = st.secrets.get("GROQ_API_KEY")
except (KeyError, FileNotFoundError):
    pass
if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    groq_api_key = str(groq_api_key).strip().strip('"').strip("'")
if not groq_api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add GROQ_API_KEY to Streamlit Cloud Settings > Secrets."
    )

model = ChatGroq(
    model="qwen/qwen3.6-27b",
    groq_api_key=groq_api_key,
    temperature=0,
)

# 1.Create prompt template
system_template = (
    "Translate the user's English text into {language}. "
    "Return only the translation. Do not include explanations, alternatives, "
    "metadata, or hidden reasoning. Preserve the original meaning and formatting."
)
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),
    ('user','{text}')
])

parser = StrOutputParser()
chain = prompt_template | model | parser

app = FastAPI(title="English Translator")
add_routes(app, chain, path="/translate")