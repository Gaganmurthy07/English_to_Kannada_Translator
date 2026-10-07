import streamlit as st
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_groq import ChatGroq

st.title("🇬🇧 English → 🇮🇳 Kannada Translator")

import streamlit as st

if "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["Prompt"]
else:

    groq_api_key = st.text_input("Enter Groq API Key", type="password")

if not groq_api_key:
    st.warning("Please provide your Groq API key in secrets or enter it above.")
    st.stop()



llm = ChatGroq(model="openai/gpt-oss-120b", temperature=1.6, api_key=api_key)

examples = [
    {"review": "How are you", "answer": "ನೀವು ಹೇಗಿದ್ದೀರಿ"},
    {"review": "Good Morning", "answer": "ಶುಭೋದಯ"},
    {"review": "The phone is okay.", "answer": "ಫೋನ್ ಪರವಾಗಿಲ್ಲ."}
]

example_prompt = PromptTemplate(
    input_variables=["review", "answer"],
    template="Review: {review}\nAnswer: {answer}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="You are an expert in Translating Text from English to Kannada. Look at the examples below.",
    suffix="Review: {review}\nAnswer:",
    input_variables=["review"]
)

chain = few_shot_prompt | llm

english_text = st.text_area("Enter English Text", placeholder="Type here...")
if st.button("Translate to Kannada", type="primary"):
    if english_text.strip():
        response = chain.invoke({"review": english_text})
        st.success(response.content)
    else:
        st.warning("Please enter text.")
