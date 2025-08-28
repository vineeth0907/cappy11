import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def load_company_data(file_path="data/capserve_info.txt"):
    """Load company information from the text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "CapServ Digital Lending is a cutting-edge digital platform aimed at modernizing financial services through a comprehensive lending marketplace."

def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks for better context retrieval."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks

def find_relevant_context(user_query, company_data, top_k=3):
    """Find the most relevant context from company data using TF-IDF and cosine similarity."""
    # Clean and prepare the query
    query_clean = re.sub(r'[^\w\s]', '', user_query.lower())
    
    # Split company data into chunks
    chunks = chunk_text(company_data)
    
    if not chunks:
        return company_data
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    try:
        tfidf_matrix = vectorizer.fit_transform(chunks + [query_clean])
        
        # Calculate similarity between query and each chunk
        query_vector = tfidf_matrix[-1]
        chunk_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(query_vector, chunk_vectors).flatten()
        
        # Get top-k most similar chunks
        top_indices = similarities.argsort()[-top_k:][::-1]
        relevant_chunks = [chunks[i] for i in top_indices if similarities[i] > 0.1]
        
        if relevant_chunks:
            return " ".join(relevant_chunks)
        else:
            return company_data[:1000]  # Return first 1000 chars if no good match
    except:
        # Fallback if vectorization fails
        return company_data[:1000]

def create_contextual_prompt(user_query, company_data):
    """Create a contextual prompt for Gemini with relevant company information."""
    relevant_context = find_relevant_context(user_query, company_data)
    
    prompt = f"""You are Cappy, the AI assistant for CapServ Digital Lending, a cutting-edge digital lending platform. 
    
Company Context:
{relevant_context}

User Question: {user_query}

Instructions:
1. Always respond as Cappy, CapServ Digital Lending's company assistant
2. Use the company context above to provide accurate information about CapServ
3. If the question is about CapServ, use the provided context
4. If it's a general financial or lending question, answer professionally while maintaining your role as CapServ's assistant
5. Keep responses helpful, professional, and aligned with CapServ's digital lending mission
6. If you don't have specific information about something, say so and offer to connect the user with a human advisor
7. Focus on digital lending, marketplace platforms, and financial technology solutions

Response:"""
    
    return prompt

def format_chat_message(role, content):
    """Format chat messages for consistent display."""
    if role == "assistant":
        return f"🤖 **Cappy:** {content}"
    elif role == "user":
        return f"👤 **You:** {content}"
    else:
        return content
