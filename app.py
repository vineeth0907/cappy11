import streamlit as st
import google.generativeai as genai
import os
from utils import load_company_data, create_contextual_prompt, format_chat_message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cappy - CapServ Digital Lending AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Modern CSS for Beautiful UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Remove Streamlit default padding and margins */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 90vw !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html { 
        font-size: 16px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    body { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #1f2937;
        background: transparent;
    }
    
    /* App container with glassmorphism effect */
    .chat-app {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        overflow: hidden;
    }
    
    /* Enhanced header with gradient and better styling */
    .app-header {
        position: relative;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 32px 24px;
        text-align: center;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .header-content {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .app-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        letter-spacing: -0.02em;
    }
    
    .app-header p {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 12px 0 0 0;
        font-weight: 400;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Welcome section with better styling */
    .welcome-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 32px 24px;
        text-align: center;
        border-bottom: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .welcome-content {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .welcome-content p {
        color: #475569;
        line-height: 1.8;
        margin: 0 0 16px 0;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    .welcome-content p:last-child {
        margin-bottom: 0;
        font-weight: 500;
        color: #334155;
    }
    
    /* Main chat area with improved styling */
    .chat-main {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        min-height: 60vh;
    }
    
    /* Chat messages container with better spacing */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 32px;
        background: transparent;
    }
    
    .messages-wrapper {
        max-width: 900px;
        margin: 0 auto;
        width: 100%;
    }
    
    /* Enhanced chat input area */
    .chat-input-area {
        background: white;
        border-top: 1px solid rgba(226, 232, 240, 0.8);
        padding: 32px 24px;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .input-container {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 16px;
        align-items: center;
    }
    
    /* Enhanced Streamlit chat input styling */
    [data-testid="stChatInput"] {
        background: white;
        border-radius: 16px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    /* Enhanced sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-right: 1px solid rgba(226, 232, 240, 0.8);
        padding: 24px 16px;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 8px;
        text-align: center;
    }
    
    [data-testid="stSidebar"] .stMarkdown h4 {
        color: #475569;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 24px 0 16px 0;
        text-align: center;
    }
    
    [data-testid="stSidebar"] hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        margin: 24px 0;
    }
    
    /* Enhanced button styling with gradients and animations */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 14px 20px;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
    }
    
    [data-testid="stSidebar"] .stButton:nth-of-type(1) > button { /* New Chat */
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton:nth-of-type(1) > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
    }
    
    [data-testid="stSidebar"] .stButton:nth-of-type(2) > button, /* Help */
    [data-testid="stSidebar"] .stButton:nth-of-type(3) > button { /* About */
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #475569;
        border: 2px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stButton:nth-of-type(2) > button:hover,
    [data-testid="stSidebar"] .stButton:nth-of-type(3) > button:hover {
        transform: translateY(-2px);
        border-color: #cbd5e1;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] .stButton:nth-of-type(4) > button { /* Clear Chat */
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton:nth-of-type(4) > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
    }
    
    /* Enhanced chat message styling */
    [data-testid="stChatMessage"] {
        margin-bottom: 24px;
        animation: slideInUp 0.4s ease;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-radius: 18px 18px 4px 18px;
        padding: 16px 20px;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 18px 18px 18px 4px;
        padding: 16px 20px;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .chat-app {
            margin: 10px;
            border-radius: 16px;
        }
        
        .app-header {
            padding: 24px 16px;
            border-radius: 16px 16px 0 0;
        }
        
        .app-header h1 {
            font-size: 2.5rem;
        }
        
        .app-header p {
            font-size: 1.1rem;
        }
        
        .welcome-section {
            padding: 24px 16px;
        }
        
        .chat-messages {
            padding: 24px 16px;
        }
        
        .chat-input-area {
            padding: 24px 16px;
        }
        
        [data-testid="stChatMessage"][data-testid*="user"],
        [data-testid="stChatMessage"][data-testid*="assistant"] {
            margin-left: 5%;
            margin-right: 5%;
        }
        
        .main .block-container {
            max-width: 100vw !important;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(241, 245, 249, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border: 3px solid #e2e8f0;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Simple, clean spinner styling */
    .stSpinner {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 16px !important;
        padding: 20px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(226, 232, 240, 0.6) !important;
    }
    
    /* Simple spinner text styling - NO ANIMATION */
    .stSpinner > div:last-child {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #475569 !important;
        text-align: center !important;
        padding: 8px 16px !important;
        background: rgba(248, 250, 252, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(226, 232, 240, 0.4) !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: unset !important;
        max-width: none !important;
        transform: none !important;
        animation: none !important;
    }
    
    /* No animation - just static display */
    .stSpinner > div:first-child {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API
def initialize_gemini():
    """Initialize the Gemini API client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        # Try different model names in order of preference (free-tier friendly first)
        model_names = ['gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro', 'gemini-1.5-pro']
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                return model
            except Exception as e:
                continue
        
        return None
        
    except Exception as e:
        return None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = initialize_gemini()

# Load company data
company_data = load_company_data()

# Enhanced app header with gradient background
st.markdown(
    """
<div class="app-header">
  <div class="header-content">
    <h1>🤖 Cappy</h1>
    <p>CapServ Digital Lending's AI Assistant</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Enhanced welcome section
st.markdown(
    """
<div class="welcome-section">
  <div class="welcome-content">
    <p>Welcome to Cappy AI Assistant. We help you connect, learn, and explore smarter conversations.</p>
    <p>Powered by AI, designed for simplicity, built for you.</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Welcome message (only show on first load)
if not st.session_state.messages:
    welcome_message = "Hi, I'm Cappy, CapServ Digital Lending's assistant. How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Enhanced sidebar with better styling
with st.sidebar:
    st.markdown("### 🤖 Cappy")
    st.markdown("---")
    st.markdown("#### Navigation")
    new_chat_clicked = st.button("New Chat", key="new_chat_btn")
    help_clicked = st.button("Help", key="help_btn")
    about_clicked = st.button("About", key="about_btn")
    st.markdown("---")
    clear_button = st.button("Clear Chat", key="clear_chat_btn")

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    role = message.get("role", "assistant")
    with st.chat_message("assistant" if role == "assistant" else "user"):
        st.markdown(message.get("content", ""))

# Enhanced chat input area
st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
user_input = st.chat_input("Type your message here…")
st.markdown('</div>', unsafe_allow_html=True)

# Handle clear chat
if clear_button:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Cappy, CapServ Digital Lending's assistant. How can I help you today?"}]
    st.rerun()

# Handle new chat
if 'new_chat_clicked' in locals() and new_chat_clicked:
    st.session_state.messages = [{"role": "assistant", "content": "New chat started. How can I help you today?"}]
    st.rerun()

# Handle send message
if user_input and user_input.strip():
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show enhanced typing indicator
    with st.spinner("🤖 Cappy is thinking..."):
        try:
            if st.session_state.gemini_model:
                # Create contextual prompt
                prompt = create_contextual_prompt(user_input, company_data)
                
                # Get response from Gemini
                response = st.session_state.gemini_model.generate_content(prompt)
                
                if response.text:
                    # Add assistant response to chat
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": "I apologize, but I'm having trouble generating a response right now. Please try again or contact our human advisors for immediate assistance."
                    })
            else:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "I'm currently experiencing technical difficulties. Please try again later or contact our support team for assistance."
                })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "I encountered an unexpected error while processing your request. Please try again or contact our support team for assistance."
            })
    
    # Clear input and rerun to show new messages
    st.rerun()
