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
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    
    /* Message styling */
    .message {
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        line-height: 1.5;
    }
    
    .message.user {
        align-self: flex-end;
        background-color: #007AFF;
        color: white;
        margin-left: 20%;
    }
    
    .message.assistant {
        align-self: flex-start;
        background-color: #F0F2F6;
        color: #111827;
        margin-right: 20%;
    }
    
    /* Input area */
    .chat-input-container {
        padding: 24px;
        border-top: 1px solid #e5e7eb;
        background-color: #ffffff;
    }
    
    .chat-input-wrapper {
        display: flex;
        gap: 12px;
        align-items: flex-end;
    }
    
    .chat-input {
        flex: 1;
        border: 1px solid #d1d5db;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 1rem;
        resize: none;
        min-height: 44px;
        max-height: 120px;
        font-family: inherit;
    }
    
    .chat-input:focus {
        outline: none;
        border-color: #007AFF;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
    }
    
    .send-button {
        background-color: #007AFF;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s;
        min-height: 44px;
    }
    
    .send-button:hover {
        background-color: #0056CC;
    }
    
    .send-button:disabled {
        background-color: #6b7280;
        cursor: not-allowed;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container { max-width: 100vw !important; }
        .header-content { width: 100vw; }
        .chat-messages { padding: 16px; }
        .chat-input-container { padding: 16px; }
        .message { max-width: 90%; }
        .message.user { margin-left: 10%; }
        .message.assistant { margin-right: 10%; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini
def initialize_gemini():
    """Initialize Gemini AI with API key."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        st.error("❌ Google API key not found. Please set GOOGLE_API_KEY in your environment variables.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        st.error(f"❌ Error initializing Gemini: {str(e)}")
        return None

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'gemini_model' not in st.session_state:
    st.session_state.gemini_model = initialize_gemini()

# Load company data
company_data = load_company_data()

# Main app interface
st.markdown('<div class="chat-app">', unsafe_allow_html=True)

# Header
st.markdown('''
<div class="app-header">
    <div class="header-content">
        <h1>🤖 Cappy</h1>
        <p>CapServ Digital Lending AI Assistant</p>
    </div>
</div>
''', unsafe_allow_html=True)

# Main chat area
st.markdown('<div class="chat-main">', unsafe_allow_html=True)

# Chat messages
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Display existing messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "assistant":
        st.markdown(f'<div class="message assistant">{format_chat_message(role, content)}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message user">{format_chat_message(role, content)}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)

# Text input
user_input = st.text_area(
    "Type your message here...",
    key="user_input",
    placeholder="Ask me anything about CapServ Digital Lending or digital lending in general...",
    label_visibility="collapsed"
)

# Send button
if st.button("Send", key="send_button", type="primary"):
    if user_input.strip() and st.session_state.gemini_model:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Create contextual prompt
        prompt = create_contextual_prompt(user_input, company_data)
        
        try:
            # Get response from Gemini
            response = st.session_state.gemini_model.generate_content(prompt)
            
            if response.text:
                # Add assistant response to chat
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "I apologize, but I couldn't generate a response at the moment. Please try again."})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"I encountered an error: {str(e)}. Please try again."})
        
        # Clear input
        st.session_state.user_input = ""
        st.rerun()
    elif not st.session_state.gemini_model:
        st.error("❌ Gemini AI is not initialized. Please check your API key.")
    else:
        st.warning("Please enter a message.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for additional info
with st.sidebar:
    st.header("ℹ️ About Cappy")
    st.write("""
    Cappy is your AI assistant for CapServ Digital Lending. 
    
    I can help you with:
    - Information about CapServ's services
    - Digital lending questions
    - Financial technology insights
    - General lending guidance
    """)
    
    st.header("🔑 Setup")
    if os.getenv('GOOGLE_API_KEY'):
        st.success("✅ API Key configured")
    else:
        st.error("❌ API Key not found")
        st.info("Set GOOGLE_API_KEY in your environment variables")
    
    st.header("📊 Chat Stats")
    st.write(f"Messages in this session: {len(st.session_state.messages)}")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
