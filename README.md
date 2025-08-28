<<<<<<< HEAD
# 🤖 Cappy - CapServ Digital Lending AI Assistant

A full-stack chatbot web application built with Streamlit and Google's Gemini AI, designed to serve as CapServ Digital Lending's intelligent digital lending assistant.

## ✨ Features

- **AI-Powered Responses**: Powered by Google's Gemini AI for intelligent, contextual conversations
- **Company Knowledge Integration**: RAG-lite system that pulls relevant Capserve information
- **ChatGPT-like Interface**: Clean, modern chat UI built with Streamlit
- **Financial Expertise**: Specialized in Capserve's services and general financial advice
- **Context Memory**: Maintains conversation history throughout the session

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google AI API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for the next step

### 3. Set Up Environment
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🏗️ Project Structure

```
Cappy/
├── app.py                 # Main Streamlit application
├── utils.py              # RAG utilities and helper functions
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── data/
    └── capserve_info.txt # Company knowledge base
```

## 🔧 How It Works

1. **User Input**: Users type questions in the chat interface
2. **Context Retrieval**: The system searches `capserve_info.txt` for relevant information
3. **AI Processing**: Relevant context is sent to Gemini AI with the user's question
4. **Response Generation**: Gemini generates a contextual response as Cappy
5. **Display**: Responses are formatted and displayed in the chat interface

## 🎯 Use Cases

- **Company Information**: Questions about CapServ's digital lending platform, services, and partnerships
- **Lending Guidance**: General lending and financial guidance (with professional disclaimers)
- **Service Inquiries**: Information about digital lending marketplace, loan processing, and financial technology solutions
- **Platform Information**: Details about the lending marketplace, partnerships, and digital processes

## 🛠️ Technical Details

- **Frontend**: Streamlit (Python web framework)
- **AI Backend**: Google Gemini AI via `google-generativeai`
- **Search**: TF-IDF vectorization with scikit-learn for context retrieval
- **Styling**: Custom CSS for ChatGPT-like appearance
- **State Management**: Streamlit session state for conversation memory

## 📝 Customization

### Adding Company Information
Edit `data/capserve_info.txt` to include:
- Company details and history
- Service descriptions
- Contact information
- FAQs and common questions

### Modifying the AI Personality
Update the prompt template in `utils.py` to change:
- Response tone and style
- Company focus areas
- Professional guidelines

## 🔒 Security Notes

- API keys are stored in environment variables (never commit `.env` files)
- The app runs locally and doesn't store conversations permanently
- All AI responses include appropriate financial disclaimers

## 🚨 Important Disclaimers

- **Not Financial Advice**: Cappy provides general information, not personalized financial advice
- **Consult Professionals**: Always consult certified financial advisors for personal decisions
- **Company Information**: Responses are based on provided company data and AI capabilities

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `.env` file contains the correct `GOOGLE_API_KEY`
2. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
3. **Streamlit Issues**: Try `streamlit cache clear` if you encounter caching problems

### Getting Help

- Check that all files are in the correct directory structure
- Verify your Google AI API key is valid and has sufficient quota
- Ensure Python 3.8+ is installed

## 📄 License

This project is for demonstration purposes. Please ensure compliance with Google AI's terms of service and applicable financial regulations.

---

**Built with ❤️ for CapServ Digital Lending**
=======
# cappy11
>>>>>>> 610757cc4b3a8bd1e094347365bd18064ace4e8f
