import os
import re

def load_company_data(file_path="data/capserve_info.txt"):
    """Load company information from the text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "CapServ Digital Lending is a cutting-edge digital platform aimed at modernizing financial services through a comprehensive lending marketplace."

def find_relevant_context_simple(user_query, company_data, top_k=3):
    """Find relevant context using simple text matching instead of TF-IDF."""
    # Clean the query
    query_words = set(re.sub(r'[^\w\s]', '', user_query.lower()).split())
    
    # Split company data into sentences
    sentences = re.split(r'[.!?]+', company_data)
    
    # Score sentences based on word overlap
    sentence_scores = []
    for sentence in sentences:
        sentence_words = set(re.sub(r'[^\w\s]', '', sentence.lower()).split())
        if sentence_words:
            overlap = len(query_words.intersection(sentence_words))
            score = overlap / len(sentence_words) if sentence_words else 0
            sentence_scores.append((score, sentence.strip()))
    
    # Sort by score and return top sentences
    sentence_scores.sort(reverse=True)
    relevant_sentences = [sentence for score, sentence in sentence_scores[:top_k] if score > 0]
    
    if relevant_sentences:
        return " ".join(relevant_sentences)
    else:
        return company_data[:1000]  # Return first 1000 chars if no good match

def create_contextual_prompt(user_query, company_data):
    """Create a contextual prompt for Gemini with relevant company information."""
    relevant_context = find_relevant_context_simple(user_query, company_data)
    
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
