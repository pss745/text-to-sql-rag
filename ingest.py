import json
import os

import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
EMBED_MODEL = "gemini-embedding-001"

chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Two collections: one for schema/glossary "context", one for NL->SQL examples
schema_collection = chroma_client.get_or_create_collection("schema_context")
examples_collection = chroma_client.get_or_create_collection("examples")


def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(model=EMBED_MODEL, contents=text)
    return result.embeddings[0].values


def ingest_tables(tables: list[dict]):
    for i, table in enumerate(tables):
        text = f"Table: {table['name']}\nDescription: {table['description']}\nColumns: {table['columns']}"
        schema_collection.add(
            ids=[f"table_{i}"],
            embeddings=[embed_text(text)],
            documents=[text],
            metadatas=[{"type": "table", "name": table["name"]}],
        )
        print(f"Ingested table: {table['name']}")


def ingest_glossary(glossary: list[dict]):
    for i, term in enumerate(glossary):
        text = f"Business term: {term['term']}\nDefinition: {term['definition']}\nSQL logic: {term['sql_logic']}"
        schema_collection.add(
            ids=[f"glossary_{i}"],
            embeddings=[embed_text(text)],
            documents=[text],
            metadatas=[{"type": "glossary", "term": term["term"]}],
        )
        print(f"Ingested glossary term: {term['term']}")


def ingest_examples(examples: list[dict]):
    for i, example in enumerate(examples):
        text = example["question"]
        examples_collection.add(
            ids=[f"example_{i}"],
            embeddings=[embed_text(text)],
            documents=[text],
            metadatas=[{"sql": example["sql"]}],
        )
        print(f"Ingested example: {example['question'][:60]}...")


def main():
    with open("data.json", "r") as f:
        data = json.load(f)

    ingest_tables(data["tables"])
    ingest_glossary(data["glossary"])
    ingest_examples(data["examples"])

    print("\nDone.")
    print(f"schema_context collection count: {schema_collection.count()}")
    print(f"examples collection count: {examples_collection.count()}")


if __name__ == "__main__":
    main()