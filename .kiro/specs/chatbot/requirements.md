# SimpleGroqChat Requirements

## Project Goal
Create a minimal, functional AI chatbot web application that demonstrates the 7 Kiro University lessons without over-engineering. The chatbot must be production-ready, easy to set up, and clearly demonstrate Kiro features for the final project submission.

## Functional Requirements

### FR1: Chat Interface
**Priority:** Critical
**Description:** Users must be able to interact with an AI chatbot through a web interface.

**Acceptance Criteria:**
- Single-page web interface with a chat area
- User can type messages in a text input field
- User can send messages by clicking a "Send" button
- User messages appear aligned to the right in the chat area
- AI responses appear aligned to the left in the chat area
- Chat history remains visible during the session
- Chat area is scrollable when messages exceed visible space

### FR2: AI Response Generation
**Priority:** Critical
**Description:** The application must call the Groq API to generate AI responses.

**Acceptance Criteria:**
- Backend successfully connects to Groq API
- User message is sent to Groq API
- AI response is returned to the frontend
- Response appears in the chat area below the user's message
- API model name is configurable via environment variable

### FR3: Loading State
**Priority:** High
**Description:** Users must see feedback while waiting for AI responses.

**Acceptance Criteria:**
- Loading indicator appears after sending a message
- Loading indicator remains visible until response arrives
- User cannot send another message while loading
- Loading indicator disappears when response is displayed

### FR4: Error Handling
**Priority:** Critical
**Description:** The application must handle errors gracefully without crashing.

**Acceptance Criteria:**
- Missing API key shows clear error message
- Invalid API responses show user-friendly error
- Network errors are caught and displayed
- Empty/whitespace-only messages are rejected
- Backend errors return meaningful error messages

### FR5: Environment Configuration
**Priority:** Critical
**Description:** Sensitive configuration must be managed securely.

**Acceptance Criteria:**
- API key stored in environment variable (GROQ_API_KEY)
- Model name stored in environment variable (GROQ_MODEL)
- `.env.example` file provides template
- `.env` file is in `.gitignore`
- API key never exposed in frontend code
- README explains how to configure environment

## API Requirements

### API1: Chat Endpoint
**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "message": "Hello"
}
```

**Response (Success):**
```json
{
  "response": "Hello! How can I help you?"
}
```

**Response (Error):**
```json
{
  "error": "Error message explaining what went wrong"
}
```

**Validation:**
- Message field is required
- Message must not be empty or whitespace-only
- Returns 400 for validation errors
- Returns 500 for server errors
- Returns 503 for Groq API errors

## UI Requirements

### UI1: Visual Design
**Theme:** Dark mode, clean and modern

**Layout:**
- Dark background (#1a1a1a or similar)
- Chat title: "SimpleGroqChat"
- Subtitle: "Powered by Groq"
- Centered chat container (max-width: 800px)
- Fixed input area at bottom
- Scrollable message area

**Messages:**
- User messages: blue/teal background, right-aligned
- AI messages: gray background, left-aligned
- Readable font size (14-16px)
- Adequate padding and spacing
- Rounded corners for message bubbles

### UI2: Interactivity
- Send button activates on click
- Enter key submits message
- Input clears after successful send
- Chat auto-scrolls to newest message
- Disable input/button while loading

## Kiro Lessons Integration

### Lesson 1: Spec-driven Development
This specification file guides all implementation.

### Lesson 2: Steering Documents
Create `.kiro/steering/project.md` with project-specific guidelines.

### Lesson 3: Hooks
Create a pre-commit hook that validates Python syntax.

### Lesson 4: Property-based Testing
Test chat message handling properties (non-empty responses, message preservation).

### Lesson 5: Powers
Use an appropriate Kiro Power for development workflow.

### Lesson 6: MCP
Configure an MCP server for development assistance.

### Lesson 7: Custom Agents
Create "Chatbot Reviewer" agent for security and quality checks.

## Non-Requirements
The following are explicitly OUT OF SCOPE:
- User authentication or accounts
- Database or persistent storage
- RAG (Retrieval Augmented Generation)
- Voice input/output
- Image generation
- Response streaming (unless trivial)
- Multiple chat sessions
- Complex UI frameworks (React, Vue, etc.)
- Containerization (Docker)
- Deployment automation

## Success Criteria
The project is complete when:
1. Chatbot sends and receives messages successfully
2. All 7 Kiro lessons are demonstrated
3. Application can be cloned and run by another person
4. README clearly explains setup and usage
5. No API keys are committed to git
6. Code is clean and readable
7. Basic tests pass
