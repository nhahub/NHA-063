# ChatOBoto - English Learning Chatbot

An intelligent multi-agent English learning chatbot built with Streamlit and LangGraph. ChatOBoto helps users practice English through conversational interactions, grammar explanations, and factual question answering.

## 🌟 Features

### Core Capabilities
- **🌐 Multi-Language Support**: Automatically detects and translates Arabic input to English
- **🎯 Intent Classification**: Intelligently routes queries to appropriate agents
- **📚 Grammar Explanations**: RAG-powered grammar explanations using educational knowledge base
- **🔍 Fact Search**: Real-time web search for factual questions
- **💬 Conversational Practice**: Natural conversation with grammar correction suggestions
- **👤 User Management**: Secure authentication with Firebase
- **💾 Chat History**: Persistent conversation history across sessions

### Agent Types
1. **Language Classifier**: Detects input language (Arabic/English)
2. **Translator**: Translates Arabic to English
3. **Intent Classifier**: Routes to appropriate service
4. **Grammar Agent**: Provides grammar explanations using RAG
5. **Fact Search Agent**: Performs web searches for factual queries
6. **Chat Agent**: Handles conversational interactions with grammar correction

## 🏗️ Architecture

The application uses a **LangGraph state machine** to orchestrate multiple AI agents:

```
User Input → Language Detection → Translation (if Arabic) → Intent Classification
                                                              ↓
                    ┌─────────────────────────────────────────┼─────────────────────────┐
                    ↓                                         ↓                         ↓
            Grammar Question                          Fact Question              Chat
                    ↓                                         ↓                         ↓
            RAG Retrieval                            Web Search              Conversational AI
                    ↓                                         ↓                         ↓
                    └─────────────────────────────────────────┼─────────────────────────┘
                                                              ↓
                                                      Final Response
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Agent Framework**: LangGraph
- **LLM Framework**: LangChain
- **AI Models**:
  - Google Gemini 2.0 Flash (Chat agent)
  - HuggingFace SmolLM3-3B (Classification)
  - GLM-4.6 (Grammar explanations)
  - Helsinki-NLP (Translation)
- **Database**: 
  - Firebase Firestore (User data & chat history)
  - ChromaDB (Knowledge base for grammar)
- **APIs**: Tavily (Web search)

## 📋 Prerequisites

- Python 3.8+
- Firebase project with Firestore enabled
- ChromaDB account (Cloud)
- API Keys:
  - HuggingFace API token
  - Tavily API key
  - Google Gemini API key
  - ChromaDB API token

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nhahub/NHA-063.git
   cd chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Streamlit secrets**

   Create a `.streamlit/secrets.toml` file with the following structure:
   ```toml
   HF_token = "your_huggingface_token"
   Travily_token = "your_tavily_api_key"
   Gemini_key = "your_google_gemini_api_key"
   Chromadb_token = "your_chromadb_api_token"
   
   [FIREBASE_KEY]
   type = "service_account"
   project_id = "your_project_id"
   private_key_id = "your_private_key_id"
   private_key = "your_private_key"
   client_email = "your_client_email"
   client_id = "your_client_id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "your_cert_url"
   ```

4. **Set up ChromaDB**
   - Ensure your ChromaDB collection named "books" exists in the "Edu_KB" database
   - The collection should contain educational materials for grammar explanations

5. **Set up Firebase**
   - Create a Firestore database
   - The application will automatically create the necessary collections:
     - `users` collection for user accounts
     - `chats` subcollection under each user for chat sessions

## 🎮 Usage

1. **Start the application**
   ```bash
   streamlit run main.py
   ```

2. **Access the application**
   - Open your browser to the URL shown in the terminal (typically `http://localhost:8501`)

3. **Create an account or login**
   - Sign up with a username, name, and password
   - Or login with existing credentials

4. **Start chatting**
   - Create a new chat from the sidebar
   - Type your message in English or Arabic
   - The system will automatically:
     - Detect the language
     - Classify your intent
     - Route to the appropriate agent
     - Provide a response

## 📁 Project Structure

```
chatbot/
├── main.py                 # Main Streamlit application entry point
├── Agents/
│   ├── graph.py           # LangGraph state machine definition
│   ├── state.py           # State schema definition
│   ├── components.py      # Agent node implementations
│   ├── Rag.py             # RAG service for grammar explanations
│   └── main.py            # (Unused - graph visualization)
├── pages/
│   └── mainpage.py        # Chat page implementation
├── widgets.py             # UI widgets (login, logout, add_chat)
├── functions.py           # Database operations (Firebase)
├── requirements.txt       # Python dependencies
└── icons/                 # Avatar icons for chat interface
    ├── user.png
    ├── assistant1.png
    └── assistant2.png
```

## 🔧 Configuration

### ChromaDB Setup
The RAG system uses ChromaDB with:
- **Database**: `Edu_KB`
- **Collection**: `books`
- **Tenant ID**: `2c00d764-53a9-4bad-9e5e-4f1bce13358d`

Ensure your ChromaDB collection contains educational materials with metadata including `file_name`.

### Firebase Structure
```
users/
  └── {username}/
      ├── name: string
      ├── password: string
      └── chats/
          └── {chat_id}/
              ├── title: string
              ├── hist: array (chat messages)
              └── chat_bot_hist: array (LangChain messages)
```

## 🎯 Intent Types

The system classifies user input into three intents:

1. **`chat`**: General conversation for English practice
2. **`grammar_question`**: Questions about English grammar rules
3. **`fact_question`**: Factual questions requiring web search

## 🔐 Security Notes

- Passwords are stored in plain text in Firebase (consider hashing for production)
- API keys should be kept secure in Streamlit secrets
- Never commit `.streamlit/secrets.toml` to version control

## 🚧 Known Limitations

- Grammar correction tool is currently a placeholder (returns "corrected grammer sentance")



