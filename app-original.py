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

# Custom CSS for ChatGPT-style interface
st.markdown("""
<style>
    /* Remove Streamlit default padding and margins */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 80vw !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    html { font-size: 18px; }
    body { font-size: 1rem; }
    
    /* App container */
    .chat-app {
        height: 100vh;
        display: flex;
        flex-direction: column;
        background-color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Fixed header */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 16px 24px;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .header-content {
        width: 80vw;
        max-width: 80vw;
        margin: 0 auto;
        text-align: center;
    }
    
    .app-header h1 {
        font-size: 1.9rem;
        font-weight: 600;
        color: #111827;
        margin: 0;
    }
    
    .app-header p {
        font-size: 1rem;
        color: #6b7280;
        margin: 4px 0 0 0;
    }
    
    /* Main chat area */
    .chat-main {
        flex: 1;
        padding-top: 80px;
        display: flex;
        flex-direction: column;
        height: calc(100vh - 80px);
    }
    
    /* Chat messages container */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 24px;
        background-color: #f9fafb;
    }
    
    .messages-wrapper {
        width: 100%;
        margin: 0 auto;
    }
    
    /* Individual chat message */
    .message {
        display: flex;
        align-items: flex-start;
        margin-bottom: 24px;
        animation: fadeIn 0.3s ease;
    }
    
    .message:last-child {
        margin-bottom: 0;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Message avatar */
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin-right: 16px;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background-color: #10b981;
        color: white;
    }
    
    .assistant-avatar {
        background-color: #3b82f6;
        color: white;
    }
    
    /* Message content */
    .message-content {
        flex: 1;
        background-color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        line-height: 1.75;
        color: #111827;
        font-size: 1.05rem;
    }
    
    .user-message .message-content {
        background-color: #f0fdf4;
        border-color: #bbf7d0;
    }
    
    .assistant-message .message-content {
        background-color: #f3f4f6; /* light black/soft gray */
        border-color: #d1d5db;
    }
    
    /* Input area */
    .input-area {
        background-color: white;
        border-top: 1px solid #e5e7eb;
        padding: 24px;
        flex-shrink: 0;
    }
    
    .input-container {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 1.05rem;
        background-color: white;
        color: #111827;
        transition: all 0.2s ease;
        flex: 1;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        outline: none;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        cursor: pointer;
        min-width: 80px;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Clear button */
    .clear-btn {
        background-color: #6b7280 !important;
    }
    
    .clear-btn:hover {
        background-color: #4b5563 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-header {
            padding: 12px 16px;
        }
        
        .chat-messages {
            padding: 16px;
        }
        
        .input-area {
            padding: 16px;
        }
        
        .input-container {
            flex-direction: column;
            gap: 12px;
        }
        
        .message-content {
            padding: 14px 16px;
            font-size: 0.9rem;
        }
    }
    
    /* Custom scrollbar */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Center Streamlit chat input to 80% width */
    [data-testid="stChatInput"] {
        max-width: 80vw;
        margin-left: auto;
        margin-right: auto;
    }

    @media (max-width: 768px) {
        .main .block-container { max-width: 100vw !important; }
        .header-content { width: 100vw; max-width: 100vw; }
        [data-testid="stChatInput"] { max-width: 100vw; }
    }

    /* Sidebar button styling */
    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 600;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        color: #111827;
        transition: all .15s ease;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    /* Order-specific accents inside sidebar */
    [data-testid="stSidebar"] .stButton:nth-of-type(1) > button { /* New Chat */
        background-color: #10b981; /* emerald */
        color: #ffffff;
        border-color: #10b981;
    }
    [data-testid="stSidebar"] .stButton:nth-of-type(1) > button:hover {
        background-color: #059669;
        border-color: #059669;
    }
    [data-testid="stSidebar"] .stButton:nth-of-type(2) > button, /* Help */
    [data-testid="stSidebar"] .stButton:nth-of-type(3) > button { /* About */
        background-color: #f9fafb;
        color: #111827;
    }
    [data-testid="stSidebar"] .stButton:nth-of-type(4) > button { /* Clear Chat */
        background-color: #ef4444; /* red */
        color: #ffffff;
        border-color: #ef4444;
    }
    [data-testid="stSidebar"] .stButton:nth-of-type(4) > button:hover {
        background-color: #dc2626;
        border-color: #dc2626;
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

# App header
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

# Spacer to offset fixed header height (slightly larger due to bigger fonts)
st.markdown("<div style='height:96px'></div>", unsafe_allow_html=True)

# About section (simple and centered)
st.markdown(
    """
<div style="max-width:800px;margin:0 auto;text-align:center;padding:8px 24px 0 24px;">
  <p style=\"color:#4b5563;line-height:1.7;margin:0 0 4px 0;\">
    Welcome to Cappy AI Assistant. We help you connect, learn, and explore smarter conversations.
  </p>
  <p style=\"color:#4b5563;line-height:1.7;margin:0 0 12px 0;\">
    Powered by AI, designed for simplicity, built for you.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# Welcome message (only show on first load)
if not st.session_state.messages:
    welcome_message = "Hi, I'm Cappy, CapServ Digital Lending's assistant. How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Sidebar like ChatGPT
with st.sidebar:
    st.markdown("### 🤖 Cappy")
    st.markdown("---")
    st.markdown("#### Navigation")
    new_chat_clicked = st.button("New Chat", key="new_chat_btn")
    help_clicked = st.button("Help", key="help_btn")
    about_clicked = st.button("About", key="about_btn")
    st.markdown("---")
    clear_button = st.button("Clear Chat", key="clear_chat_btn")

# Display chat messages
for message in st.session_state.messages:
    role = message.get("role", "assistant")
    with st.chat_message("assistant" if role == "assistant" else "user"):
        st.markdown(message.get("content", ""))

# Native chat input at bottom
user_input = st.chat_input("Type your message here…")

# Auto-scroll the input area into view on load/rerun
# Native components handle scrolling; no custom JS needed

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
    
    # Show typing indicator
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
