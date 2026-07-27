## 1. Problem Statement
Business users need to ask questions in plain English (e.g. "how many active loans are in Texas") and get back a correct SQL query against a mortgage servicing database — without knowing table names, column names, or internal business logic (e.g. what counts as "active" or "delinquent").

A plain LLM call fails at this because:

It doesn't know your actual table/column names → hallucinates them
It doesn't know your business definitions (e.g. "Active Loan Portfolio" = a specific status IN (...) condition, not just status = 'ACTIVE')
It has no way to say "I don't know" — it just guesses and gives a random SQL snippet

Solution: Retrieval-Augmented Generation (RAG). Instead of asking the LLM to know everything upfront, we give it only the relevant schema, business rules, and past examples for each specific question, retrieved fresh from a knowledge base at query time.


## 2. Architecture

