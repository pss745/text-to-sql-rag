# RAG - Retrieval Augmented Generation:

RAG is an architecture which enhances LLM’s by providing them with domain specific external knowledge sources, enabling them access to up to date information for more accurate and relevant information., reducing hallucinations.

## How it works?

Query Processing : The input query(Ex: “How many states are in the USA?”) is preprocessed and made into embeddings.
Embedding Model : The query is passed into an embedding model and that converts it into a vector capturing its semantic meaning.
Vector DB Retrieval : This vector is used to search a vector DB and find content that are most similar to the query.
LLM Response : The LLM combines the query with retrieved context to generate an accurate response.
Response : The final response integrates model’s internal  knowledge and retrieved information.

## Important concepts in this process:

Embedding Models: Embedding models are a type of ML models to represent data (text, images, etc) in a continuous low dimensional vector space. These embeddings  capture semantic  meanings between pieces of data enabling machines to perform tasks like, comparison more effectively.
Ex: Apple can be[1,2,3] and a Banana can be [1,2,5], these embeddings can be used to compare fruits or group similar fruits.


Vector DB’s: Imagine a Point A which connects to Point B, this arrow is what you need to carry point A to point B. Vector is like an arrow. This arrow will have both distance and direction.

A vector space is a set of vectors that can be played with each other. You can add or multiply them, but need to follow some certain rules.

A vector dimension , this is  a way to describe how many directions something is measured.
Ex: Both Latitude and Longitude is required to locate a point/place on the sphere.

## References: 
https://learn.microsoft.com/en-us/data-engineering/playbook/solutions/vector-database/
https://www.couchbase.com/blog/embedding-models/

