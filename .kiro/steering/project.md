# SimpleGroqChat Project Guidelines

## Overview
This steering document provides guidelines for Kiro when working on the SimpleGroqChat project. Follow these principles to ensure consistency with the project's goals and architecture.

## Technology Stack Guidelines

### Backend
- **Use Python Flask** - Keep the backend simple with minimal dependencies
- **Use python-dotenv** for environment variable management
- **Use groq** official SDK for API integration
- **Do NOT** add unnecessary frameworks like Django, FastAPI, or async libraries

### Frontend
- **Use vanilla HTML/CSS/JavaScript** - No React, Vue, Angular, or other frameworks
- **Keep styling simple** - No CSS frameworks like Bootstrap, Tailwind, or Material-UI
- **Use modern JavaScript** - ES6+ features are fine, but avoid complex build tools

## Security Guidelines

### API Key Management
- **NEVER expose API keys in frontend code** - All sensitive data stays on the backend
- **Use environment variables** for all configuration
- **Always include .env in .gitignore** - No exceptions
- **Provide .env.example** with placeholder values

### Input Validation
- **Validate all user inputs** on the backend
- **Sanitize inputs** before sending to external APIs
- **Return meaningful error messages** without exposing internal details

## Code Quality Guidelines

### Readability
- **Prefer readable code over clever code** - The project should be easy to understand
- **Use clear variable and function names** - Avoid abbreviations
- **Add comments for complex logic** - Explain the "why", not just the "what"
- **Keep functions small** - Each function should do one thing well

### Structure
- **Follow the existing project structure** - Don't reorganize unnecessarily
- **Keep changes small** - Make incremental, testable changes
- **Use consistent formatting** - Follow Python PEP 8 and standard web formatting

### Dependencies
- **Avoid unnecessary dependencies** - Only add packages that are truly needed
- **Pin dependency versions** - Use specific versions in requirements.txt
- **Keep the dependency list minimal** - This is a simple project, keep it that way

## Development Process

### File Organization
- **Flask app in app.py** - Single file for simplicity
- **Templates in templates/** - Standard Flask convention
- **Static files in static/** - CSS and JS files
- **Kiro config in .kiro/** - Specs, hooks, agents, steering documents

### Error Handling
- **Handle all error cases** - Network errors, API errors, validation errors
- **Provide user-friendly error messages** - No technical details exposed to users
- **Log errors appropriately** - Use Python logging for debugging
- **Fail gracefully** - The app should never crash

### Testing
- **Test core functionality** - Ensure the chatbot works end-to-end
- **Test error cases** - Missing API key, invalid input, API failures
- **Use property-based testing** for Kiro lesson demonstration
- **Keep tests simple** - Focus on functionality, not test complexity

## Kiro Lesson Integration

### Spec-driven Development
- **Follow the specification** - All implementation should match requirements.md and design.md
- **Update specs if needed** - If requirements change, update the spec first

### Hooks
- **Keep hooks simple** - Lightweight syntax checks or linting
- **Focus on Python files** - The main codebase is Python

### Powers and MCP
- **Choose simple, relevant tools** - Don't add complexity for its own sake
- **Document actual usage** - Only claim features that are genuinely used

### Custom Agents
- **Give agents specific purposes** - Clear, limited responsibilities
- **Grant minimal necessary permissions** - Only the tools they actually need

## Project Constraints

### Simplicity First
- **This is a demonstration project** - Prioritize working functionality over perfection
- **Time is limited** - Don't over-engineer solutions
- **Focus on the 7 Kiro lessons** - Each lesson should be clearly demonstrated

### Scope Limitations
- **No user authentication** - Out of scope
- **No database** - Chat history is session-only
- **No advanced features** - No RAG, voice, images, streaming (unless trivial)
- **No deployment complexity** - Keep it runnable with simple commands

## Success Criteria

A task is complete when:
1. It meets the acceptance criteria in tasks.md
2. The code is readable and follows these guidelines
3. All tests pass (if applicable)
4. The feature integrates cleanly with existing code
5. No new security vulnerabilities are introduced

## Common Pitfalls to Avoid

- Adding unnecessary complexity
- Exposing API keys in frontend
- Over-engineering the UI
- Adding features not in requirements
- Breaking the simple Flask structure
- Forgetting to handle error cases
- Not testing with actual Groq API

## When in Doubt

- **Refer to the spec** - requirements.md and design.md have the answers
- **Keep it simple** - The simpler solution is usually better
- **Focus on working code** - Perfect is the enemy of done
- **Test early and often** - Catch issues before they become problems