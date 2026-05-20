from fastapi import FastAPI, UploadFile, File
import shutil
import os
from pydantic import BaseModel
from services.embeddings import create_query_embedding
from services.vector_store import clear_vector_store, search_similar
from services.llm import generate_answer
from services.pdf_parser import extract_text_from_pdf
from services.chunker import chunk_text
from services.embeddings import create_embeddings
from services.vector_store import store_embeddings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
chat_history = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QuestionRequest(BaseModel):
    question: str
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.get("/")
def home():
    return {"message": "RAG Chatbot Backend Running"}
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Extract text
    text = extract_text_from_pdf(file_path)
    if not text.strip():
        return {
            "error": "Could not extract text from PDF."
        }
    # Chunk text
    chunks = chunk_text(text)
    if len(chunks) == 0:
        return {
            "error": "No chunks created."
        }
    # Create embeddings
    embeddings = create_embeddings(chunks)
    # Store embeddings
    store_embeddings(
        embeddings,
        chunks,
        file.filename
    )
    return {
        "message": "Document uploaded successfully",
        "chunks_created": len(chunks)
    }
@app.post("/chat")
async def chat(request: QuestionRequest):
    question = request.question
    # Create query embedding
    query_embedding = create_query_embedding(question)
    # Retrieve relevant chunks
    retrieved_chunks = search_similar(query_embedding)
    if len(retrieved_chunks) == 0:
        return {
            "question": question,
            "answer": (
                "This question is outside the scope "
                "of the uploaded documents."
            ),
            "confidence": 0,
            "sources": []
        }
    # Combine chunks into context
    top_paragraphs = []
    for chunk in retrieved_chunks:
        paragraph = chunk["chunk"].strip()
        top_paragraphs.append(paragraph)
    document_context = "\n".join(top_paragraphs)

    history_context = ""
    for item in chat_history[-5:]:
        history_context += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n"
        )

    context = f"""
Conversation History:
{history_context}

Document Context:
{document_context}
"""
    # Generate answer
    raw_score = retrieved_chunks[0]["score"] if retrieved_chunks else 0
    # Better scaling for cosine similarity
    confidence = min(
        round((raw_score + 1) * 50, 2),
        99.9
    )
    answer = generate_answer(question, context)
    chat_history.append({
        "question": question,
        "answer": answer
    })
    if len(chat_history) > 10:
        chat_history.pop(0)
    clean_sources = []

    for chunk in retrieved_chunks:
        clean_sources.append({
            "file": chunk["filename"],
            "text": chunk["chunk"],
            "score": round(chunk["score"] * 100, 2)
})

    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "sources": clean_sources
    }