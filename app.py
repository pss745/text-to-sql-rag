import streamlit as st

from query import generate_sql

st.title("Text-to-SQL")

question = st.text_input("Ask a question about the loan portfolio:")

if st.button("Generate SQL") and question:
    with st.spinner("Generating SQL..."):
        sql = generate_sql(question)
    st.code(sql, language="sql")