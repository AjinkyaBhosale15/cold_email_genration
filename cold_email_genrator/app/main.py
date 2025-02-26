import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain.document_loaders import WebBaseLoader  # ✅ Added import

# Set page config (must be the first Streamlit command)
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

# Initialize objects before using them
portfolio = Portfolio()  # ✅ Initialize Portfolio early
llm = Chain()  # ✅ Initialize Chain (assuming it handles LLM functions)

st.title("Cold Mail Generator")

url_input = st.text_input("Enter a URL:", value="https://careers.ibm.com/job/20978143/software-developer-intern-2025-san-jose-ca/?codes=WEB_Search_INDIA")
submit_button = st.button("Submit")

if submit_button:
    try:
        loader = WebBaseLoader([url_input])
        data = clean_text(loader.load().pop().page_content)

        portfolio.load_portfolio()
        jobs = llm.extract_jobs(data)

        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)
            st.code(email, language='markdown')
    except Exception as e:
        st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    pass  # No need to reinitialize portfolio and chain
