"""
SimpleGroqChat - A minimal AI chatbot using Flask and Google Gemini API
Demonstrates Kiro University lessons with clean, readable code.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Validate environment configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

# Initialize Gemini client if API key is available
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel(GEMINI_MODEL)
        logger.info("Gemini client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {str(e)}")
        gemini_model = None
else:
    logger.warning("GEMINI_API_KEY not found in environment variables")


@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the frontend.
    
    Expected JSON payload:
    {
        "message": "User's message text"
    }
    
    Returns:
    {
        "response": "AI response text"
    }
    OR
    {
        "error": "Error description"
    }
    """
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        # Get message from request
        data = request.get_json()
        
        # Validate message field exists
        if 'message' not in data:
            return jsonify({"error": "Message field is required"}), 400
        
        message = data.get('message')
        
        # Validate message is a string
        if not isinstance(message, str):
            return jsonify({"error": "Message must be a string"}), 400
        
        # Validate message is not empty
        message = message.strip()
        if not message:
            return jsonify({"error": "Message is required and cannot be empty"}), 400
        
        # Check API key configuration
        if not gemini_model:
            logger.error("Gemini client not available - API key missing or invalid")
            return jsonify({"error": "Chat service not configured. Please contact administrator."}), 500
        
        # Call Gemini API
        try:
            response = gemini_model.generate_content(message)
            
            # Extract response text
            if response and response.text:
                response_text = response.text.strip()
                if not response_text:
                    response_text = "I apologize, but I couldn't generate a response. Please try again."
            else:
                response_text = "I apologize, but I couldn't generate a response. Please try again."
                
            return jsonify({"response": response_text}), 200
            
        except Exception as gemini_error:
            # Log the specific Gemini API error
            logger.error(f"Gemini API error: {str(gemini_error)}")
            
            # Return user-friendly error without exposing API details
            return jsonify({"error": "Sorry, the AI service is temporarily unavailable. Please try again later."}), 503
        
    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        
        # Return generic error message to client
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == '__main__':
    # Check if we're in development mode
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting SimpleGroqChat server...")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Gemini model: {GEMINI_MODEL}")
    
    # Run the Flask development server
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)