#### Application Workflow

1. **User Request:** A user enters a natural language prompt via the Streamlit UI (e.g., *"How many active loans are in the state of Texas?"*).
2. **Context Retrieval:** The query pipeline retrieves relevant schema definitions, business logic, and similar SQL examples from the local vector database (`ChromaDB`).
3. **SQL Generation:** The LLM generates the targeted SQL query (e.g., `SELECT * FROM Database WHERE state = 'TX' AND status = 'active'`).
4. **Logging & Evaluation:** Inputs and output SQL are recorded for future evaluation datasets.

---

### Codebase Overview

#### 1. Data Source (`data.json`)

Acts as the static knowledge base. Contains database table definitions, business term glossaries, and few-shot natural language to SQL example pairs.

#### 2. User Interface (`app.py`)

The main entry point for the application. Built with Streamlit, it provides a web-based chat interface where users can submit questions and view generated SQL queries in real time.

#### 3. Execution Logging (`logger.py`)

Captures all user inputs and generated SQL outputs, logging them directly into a structured Excel spreadsheet. This dataset serves as a benchmark for setting up evaluation (evals) frameworks at later stages.

#### 4. Data Ingestion (`ingest.py`)

Converts local schema metadata, business terminology, and example SQL queries into vector embeddings and ingests them into a local ChromaDB instance. **This script must be run once as a pre-process before launching the app.**

* **Initialize Vector Storage:** Sets up a persistent local ChromaDB instance at `./chroma_db`.
* **Create Collections:** Instantiates two distinct vector collections:
* `schema_context`: Holds database table schemas and business glossary definitions.
* `examples`: Holds natural language questions paired with target SQL queries.


* **Initialize Gemini Client:** Connects to the Gemini API using `google-genai` and configures the `gemini-embedding-001` model.
* **Embedding Helper (`embed_text`):** Converts input strings into high-dimensional numerical vectors using the Gemini Embedding API.
* **Data Ingestion Functions:**
* `ingest_tables()`: Formats database structures, embeds them, and adds them to `schema_context`.
* `ingest_glossary()`: Formats business rules, embeds them, and adds them to `schema_context`.
* `ingest_examples()`: Embeds natural language questions and saves target SQL queries as metadata in `examples`.


* **Execution (`main`):** Loads `data.json`, runs all ingestion pipelines, and logs final record counts stored in ChromaDB.

#### 5. Vector Search & SQL Generation (`query.py`)

* **Initialize Models:** Sets up the `gemini-embedding-001` embedding model and the `gemini-3.5-flash` generation model.
* **Connect to Storage:** Loads the persistent `schema_context` and `examples` collections from ChromaDB.
* **Embed User Input:** Converts the incoming user query into a vector representation using an embedding helper function.
* **Retrieve Context (`retrieve_context`):** Performs a similarity search against ChromaDB to extract top matching table schemas, glossary definitions, and few-shot SQL examples.
* **Build System Prompt (`build_prompt`):** Dynamically constructs a prompt injecting the retrieved context, database rules, and user query.
* **Generate SQL (`generate_sql`):** Passes the constructed prompt to Gemini to produce the final, syntactically correct SQL query.

---
