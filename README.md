# SimpleGroqChat

A minimal AI chatbot web application demonstrating the 7 Kiro University lessons with clean, production-ready code.

## What it does

SimpleGroqChat is a single-page web application that allows users to chat with AI through a clean, dark-themed interface. Users type messages, click Send, and receive AI responses powered by Google's Gemini API. Chat history remains visible during the session.

## Features

- **Real-time AI chat** - Instant responses from Groq API
- **Clean dark UI** - Modern, responsive design
- **Error handling** - Graceful handling of network and API errors
- **Input validation** - Prevents empty messages and handles edge cases
- **Loading states** - Visual feedback during API calls
- **Session persistence** - Chat history maintained during session

## Tech Stack

- **Backend**: Python 3.8+, Flask, python-dotenv, google-generativeai
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: Google Gemini API for AI responses
- **Testing**: pytest, hypothesis for property-based testing

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure GEMINI_API_KEY

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

**Supported models:**
- `gemini-1.5-flash` (recommended - fast and efficient)
- `gemini-1.5-pro` (more capable, slower)
- `gemini-pro` (standard model)

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Kiro Lessons Demonstrated

### Spec-driven Development
Complete specification created in `.kiro/specs/chatbot/` with requirements, design, and tasks that guided all implementation.

### Steering Documents
Project guidelines in `.kiro/steering/project.md` provide clear direction for technology choices, security practices, and code quality standards.

### Hooks
Automatic Python syntax checking hook in `.kiro/hooks/` runs `py_compile` when Python files are edited to catch errors early.

### Property-based Testing
Hypothesis-based tests in `test_properties.py` verify key system properties like valid messages producing responses and proper error handling.

### Powers
Evaluated AWS Blocks Power but chose not to use it to maintain project simplicity, demonstrating appropriate technology selection for project scope.

### MCP
Configured filesystem MCP server in `.kiro/mcp_servers.json` for local file operations during development.

### Custom Agents
Created "Chatbot Reviewer" agent in `.kiro/agents/chatbot-reviewer.json` specialized for security, code quality, and requirement compliance reviews.

## Testing

Run the property-based tests:
```bash
pytest test_properties.py -v
```

## Project Structure

```
SimpleGroqChat/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
├── test_properties.py    # Property-based tests
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
└── .kiro/
    ├── specs/            # Kiro specifications
    ├── steering/         # Project guidelines
    ├── hooks/            # Automated actions
    ├── agents/           # Custom agent config
    └── mcp_servers.json  # MCP configuration
```

## Security Notes

- API key is stored in environment variables only
- `.env` file is in `.gitignore` to prevent accidental commits
- No sensitive data exposed in frontend JavaScript
- Input validation on both frontend and backend
- Error messages don't expose internal details

## Troubleshooting

**"Chat service not configured" error:**
- Check that `.env` file exists and contains `GEMINI_API_KEY`
- Verify your Gemini API key is valid
- Get a free API key at: https://makersuite.google.com/app/apikey

**"Cannot connect to the server" error:**
- Ensure Flask app is running on port 5000
- Check firewall/antivirus settings

**Empty responses:**
- Try a different Gemini model in `.env`
- Check Gemini API status and quotas

## Demo Video Highlights

Show these features in your demo:
1. **Basic Chat** - Send a message and receive AI response
2. **Error Handling** - Try empty message to show validation
3. **Kiro Features** - Point out the `.kiro/` directory structure
4. **Code Quality** - Highlight clean, readable code structure
5. **Testing** - Run `pytest test_properties.py` to show property-based tests

## Git Commands for Submission

```bash
# Initialize git (if not already done)
git init

# Add all files (note: .env is automatically excluded by .gitignore)
git add .

# Make initial commit
git commit -m "SimpleGroqChat: Complete implementation with 7 Kiro lessons"

# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/yourusername/SimpleGroqChat.git

# Push to repository
git push -u origin main
```

## License

This project is created for educational purposes as part of the Kiro University Challenge.