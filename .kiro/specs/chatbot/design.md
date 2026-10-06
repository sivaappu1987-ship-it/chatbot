# SimpleGroqChat Design

## Architecture Overview

### System Architecture
```
Browser (Frontend)
    ↓ HTTP POST
Flask Backend (app.py)
    ↓ API Call
Groq API
    ↓ Response
Flask Backend
    ↓ JSON Response
Browser (Updates UI)
```

**Architecture Style:** Simple client-server with RESTful API

**Rationale:** Minimal complexity, standard pattern, easy to understand and debug.

## Technology Stack

### Backend
- **Python 3.8+**: Well-supported, readable, simple
- **Flask**: Lightweight web framework, minimal boilerplate
- **python-dotenv**: Environment variable management
- **groq**: Official Groq Python SDK

### Frontend
- **HTML5**: Standard markup
- **CSS3**: Custom styling, no frameworks
- **Vanilla JavaScript**: No build step, no dependencies

### Rationale
This stack requires zero build tools, no complex configuration, and can be run immediately after `pip install`. Perfect for time-constrained projects.

## Project Structure

```
SimpleGroqChat/
├── app.py                 # Flask application (backend)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Actual environment (gitignored)
├── .gitignore            # Git exclusions
├── README.md             # Setup and usage
├── templates/
│   └── index.html        # Single-page frontend
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
└── .kiro/
    ├── specs/
    │   └── chatbot/
    │       ├── requirements.md
    │       ├── design.md
    │       └── tasks.md
    ├── steering/
    │   └── project.md    # Project guidelines
    ├── hooks/
    │   └── python-check.json  # Syntax validation hook
    └── agents/
        └── chatbot-reviewer.json  # Custom agent config
```

## Component Design

### 1. Flask Backend (app.py)

**Responsibilities:**
- Serve HTML page
- Handle `/api/chat` endpoint
- Validate incoming messages
- Call Groq API
- Return responses or errors

**Key Functions:**
```python
@app.route('/')
def index():
    """Serve the frontend"""

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    # 1. Validate message
    # 2. Call Groq API
    # 3. Return response or error
```

**Error Handling:**
- Catch missing API key → return 500 with clear message
- Catch validation errors → return 400
- Catch Groq API errors → return 503 with error details
- Catch unexpected errors → return 500 with generic message

**Environment Variables:**
- `GROQ_API_KEY`: API authentication
- `GROQ_MODEL`: Model name (e.g., "mixtral-8x7b-32768")

### 2. Frontend (index.html)

**Structure:**
```html
<div class="container">
  <header>
    <h1>SimpleGroqChat</h1>
    <p>Powered by Groq</p>
  </header>
  
  <div id="chat-area">
    <!-- Messages appear here -->
  </div>
  
  <div class="input-area">
    <input id="message-input" />
    <button id="send-button">Send</button>
  </div>
</div>
```

**DOM Manipulation:**
- Append user message to chat area
- Show loading indicator
- Fetch response from `/api/chat`
- Append AI response
- Remove loading indicator
- Scroll to bottom
- Clear input field

### 3. Styling (style.css)

**Design Tokens:**
- Background: `#1a1a1a` (dark)
- Container: `#252525` (lighter dark)
- User message: `#2563eb` (blue)
- AI message: `#404040` (gray)
- Text: `#ffffff` (white)
- Font: system font stack

**Layout:**
- Flexbox for message alignment
- Fixed positioning for input area
- Scrollable chat area with `overflow-y: auto`

### 4. Frontend Logic (script.js)

**Event Handlers:**
```javascript
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});
```

**Core Function:**
```javascript
async function sendMessage() {
  // 1. Get message text
  // 2. Validate not empty
  // 3. Disable input/button
  // 4. Add user message to UI
  // 5. Show loading
  // 6. POST to /api/chat
  // 7. Add AI response to UI
  // 8. Remove loading
  // 9. Enable input/button
  // 10. Handle errors
}
```

## API Design

### POST /api/chat

**Request:**
```json
{
  "message": "string (required, non-empty)"
}
```

**Response (200 OK):**
```json
{
  "response": "AI generated response text"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Message is required and cannot be empty"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "GROQ_API_KEY not configured"
}
```

**Response (503 Service Unavailable):**
```json
{
  "error": "Groq API error: [details]"
}
```

## Groq API Integration

**SDK Usage:**
```python
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
completion = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=[{"role": "user", "content": user_message}]
)
response_text = completion.choices[0].message.content
```

**Supported Models:**
- mixtral-8x7b-32768
- llama-3.1-8b-instant
- gemma2-9b-it
(Use environment variable for flexibility)

## Kiro Configuration Design

### Steering Document (.kiro/steering/project.md)
Guidelines for Kiro when working on this project:
- Use Python Flask
- Keep everything simple
- Use vanilla HTML/CSS/JS
- Never expose API keys
- Prefer readable code
- Follow existing structure

### Hook (.kiro/hooks/python-check.json)
**Trigger:** File edited (*.py)
**Action:** Run Python syntax check
**Command:** `python -m py_compile <file>`

### Custom Agent (.kiro/agents/chatbot-reviewer.json)
**Name:** Chatbot Reviewer
**Purpose:** Review for security, quality, and requirements compliance
**Tools:** read_file, grep_search, get_diagnostics

## Testing Strategy

### Property-based Tests
Test properties using Kiro's PBT capability:
- **Property 1:** Valid user input always produces non-empty response
- **Property 2:** Chat messages are never lost during UI updates
- **Property 3:** API errors always return valid JSON with error field

### Manual Tests
- Send message and receive response
- Test with empty message
- Test with missing API key
- Test with invalid API key
- Test rapid message sending
- Test long messages
- Test special characters

## Security Considerations

1. **API Key Protection:**
   - Never in frontend code
   - Never in git repository
   - Only in environment variables

2. **Input Validation:**
   - Sanitize user input (though Groq handles this)
   - Reject empty messages
   - Limit message length if needed

3. **Error Messages:**
   - Don't expose sensitive details in errors
   - Generic messages for unexpected errors

## Deployment Considerations
(Out of scope for this project, but for reference)
- Set environment variables in hosting platform
- Use HTTPS in production
- Consider rate limiting
- Monitor API usage

## Success Metrics
- Application starts without errors
- User can send message and get response
- All error cases handled gracefully
- All 7 Kiro lessons demonstrated
- Another person can clone and run the project
