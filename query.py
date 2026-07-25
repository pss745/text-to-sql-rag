import os
import traceback

import chromadb
from dotenv import load_dotenv
from google import genai

print("SCRIPT STARTED", flush=True)

load_dotenv()
print("ENV LOADED, key present:", bool(os.environ.get("GEMINI_API_KEY")), flush=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
EMBED_MODEL = "gemini-embedding-001"
GEN_MODEL = "gemini-3.5-flash"

print("CREATING GENAI CLIENT", flush=True)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
print("CHROMA CLIENT READY", flush=True)
schema_collection = chroma_client.get_collection("schema_context")
examples_collection = chroma_client.get_collection("examples")
print("COLLECTIONS LOADED:", schema_collection.count(), examples_collection.count(), flush=True)


def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(model=EMBED_MODEL, contents=text)
    return result.embeddings[0].values


def retrieve_context(question: str, n_schema: int = 4, n_examples: int = 3):
    query_vector = embed_text(question)

    schema_results = schema_collection.query(
        query_embeddings=[query_vector],
        n_results=n_schema,
    )
    example_results = examples_collection.query(
        query_embeddings=[query_vector],
        n_results=n_examples,
    )

    schema_chunks = schema_results["documents"][0]

    example_chunks = []
    for doc, meta in zip(example_results["documents"][0], example_results["metadatas"][0]):
        example_chunks.append(f"Q: {doc}\nSQL: {meta['sql']}")

    return schema_chunks, example_chunks


def build_prompt(question: str, schema_chunks: list[str], example_chunks: list[str]) -> str:
    schema_text = "\n\n".join(schema_chunks)
    examples_text = "\n\n".join(example_chunks)

    prompt = f"""You are a SQL expert for a Snowflake mortgage servicing database.

STRICT RULES:
1. You may ONLY use tables and columns that appear explicitly in the "Relevant schema and business rules" section below. Do not use any other table or column, even if it seems like a common or obvious field (e.g. do not assume "state", "region", "city", or similar fields exist unless you see them listed).
2. If the question requires a table, column, or piece of information that is NOT present in the schema below, do NOT guess or invent it. Instead, respond with exactly:
   NOT_ENOUGH_SCHEMA_INFO: <brief explanation of what's missing>
3. Do not use any column from the "Similar past questions" examples unless that same column also appears in the schema section.

## Relevant schema and business rules:
{schema_text}

## Similar past questions and their SQL:
{examples_text}

## New question:
{question}

Return ONLY the SQL query (or the NOT_ENOUGH_SCHEMA_INFO line). No explanation, no markdown formatting, no backticks.
"""
    return prompt


def generate_sql(question: str) -> str:
    schema_chunks, example_chunks = retrieve_context(question)
    prompt = build_prompt(question, schema_chunks, example_chunks)

    response = client.models.generate_content(model=GEN_MODEL, contents=prompt)
    return response.text.strip()


def main():
    question = input("Ask a question: ")
    sql = generate_sql(question)
    print("\nGenerated SQL:\n")
    print(sql)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("ERROR OCCURRED:", flush=True)
        traceback.print_exc()
    input("\nPress Enter to close...")