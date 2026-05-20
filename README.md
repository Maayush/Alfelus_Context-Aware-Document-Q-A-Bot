Context-Aware Document Q&A Bot is a RAG chatbot that uses AI to let the user upload PDF documents and ask queries related to those documents. The bot uses vector embeddings to find the most relevant chunks from the uploaded document and answers the queries using an LLM.

Features:
Upload One or Several PDF Files
AI-Powered Question Answering
Contextualized Responses
Confidence Level for Responses
Sources Citation in Responses
Highlighted Paragraph in Responses
Out-of-Context Question Detection
Latest ChatGPT Style UI
Multi-document Information Retrieval
FastAPI & React Architecture
Semantic Search Using Vector Embedding

Tech Stack:

Frontend:
React.js
Vite
Axios
CSS
React Icons

Backend:
FastAPI
Python
Sentence Transformers
HuggingFace Transformers
NumPy

AI / RAG Components:
Embeddings Model
Vector Similarity Search
Retrieval-Augmented Generation (RAG)

Project Architecture:
<img width="1191" height="931" alt="image" src="https://github.com/user-attachments/assets/30fc8f14-097d-4b73-b0be-3243d3d76a05" />

How to Use:
Upload one or more PDF documents
Ask questions related to uploaded documents
System retrieves relevant content
AI generates contextual answers
Confidence score and sources are displayed

Sample Questions:
What is the document about?
What skills are mentioned?
Who is the applicant?
What projects are included?
What languages are known?

Key Functionalities:

Retrieval-Augmented Generation (RAG)
The system combines semantic search with LLM-based answer generation to improve accuracy and contextual understanding.

Semantic Search
Embeddings are generated for document chunks and compared using cosine similarity.

Confidence Scoring
Each response includes a confidence percentage based on similarity scores.

Source Highlighting
Relevant document paragraphs are shown as references for transparency.

Future Enhancements:
Chat History Memory
Streaming Responses
Better Vector Databases (FAISS / ChromaDB)
OCR Support for Scanned PDFs
User Authentication
Cloud Deployment
Voice-Based Queries
Document Summarization

Output:
<img width="1902" height="866" alt="image" src="https://github.com/user-attachments/assets/29303a79-7483-456e-8270-64104dfd322e" />
<img width="1910" height="842" alt="image" src="https://github.com/user-attachments/assets/2802f458-7ab7-4c2e-a1fb-cb19e1b69fe3" />


Author

MADHAVARAM AAYUSH
