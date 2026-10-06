/**
 * SimpleGroqChat Frontend JavaScript
 * Handles chat functionality with clean, readable code
 */

// DOM Elements
let messageInput;
let sendButton;
let chatArea;
let loadingIndicator;
let errorModal;
let errorMessage;

// State
let isLoading = false;

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM element references
    messageInput = document.getElementById('message-input');
    sendButton = document.getElementById('send-button');
    chatArea = document.getElementById('chat-area');
    loadingIndicator = document.getElementById('loading');
    errorModal = document.getElementById('error-modal');
    errorMessage = document.getElementById('error-message');
    
    // Verify all elements exist
    if (!messageInput || !sendButton || !chatArea) {
        console.error('Required DOM elements not found');
        return;
    }
    
    // Add event listeners
    setupEventListeners();
    
    // Focus on input
    messageInput.focus();
    
    console.log('SimpleGroqChat initialized');
});

/**
 * Set up all event listeners
 */
function setupEventListeners() {
    // Send button click
    sendButton.addEventListener('click', handleSendMessage);
    
    // Enter key in input field
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    });
    
    // Prevent form submission on enter
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
        }
    });
}

/**
 * Handle sending a message
 */
async function handleSendMessage() {
    // Prevent sending if already loading
    if (isLoading) {
        return;
    }
    
    // Get message text and validate
    const message = messageInput.value.trim();
    if (!message) {
        showError('Please enter a message before sending.');
        return;
    }
    
    // Check message length
    if (message.length > 1000) {
        showError('Message is too long. Please keep it under 1000 characters.');
        return;
    }
    
    try {
        // Set loading state
        setLoadingState(true);
        
        // Add user message to chat
        addMessageToChat(message, 'user');
        
        // Clear input
        messageInput.value = '';
        
        // Send message to backend
        const response = await sendMessageToAPI(message);
        
        // Add AI response to chat
        if (response.response) {
            addMessageToChat(response.response, 'ai');
        } else if (response.error) {
            showError(`Error: ${response.error}`);
        } else {
            showError('Received an unexpected response from the server.');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        showError('Failed to send message. Please check your connection and try again.');
    } finally {
        // Reset loading state
        setLoadingState(false);
    }
}

/**
 * Send message to the backend API
 * @param {string} message - The message to send
 * @returns {Promise<Object>} - The API response
 */
async function sendMessageToAPI(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message
        })
    });
    
    // Check if response is ok
    if (!response.ok) {
        // Try to get error message from response
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
}

/**
 * Add a message to the chat area
 * @param {string} text - The message text
 * @param {string} type - 'user' or 'ai'
 */
function addMessageToChat(text, type) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    // Create message content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    // Create timestamp
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = type === 'user' ? 'You' : 'AI';
    
    // Append elements
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    // Add to chat area
    chatArea.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Set loading state
 * @param {boolean} loading - Whether loading is active
 */
function setLoadingState(loading) {
    isLoading = loading;
    
    // Update UI elements
    sendButton.disabled = loading;
    messageInput.disabled = loading;
    
    // Show/hide loading indicator
    if (loadingIndicator) {
        loadingIndicator.classList.toggle('hidden', !loading);
    }
    
    // Update button text
    sendButton.textContent = loading ? 'Sending...' : 'Send';
    
    // Update input placeholder
    messageInput.placeholder = loading ? 'AI is responding...' : 'Type your message here...';
}

/**
 * Scroll chat area to bottom
 */
function scrollToBottom() {
    chatArea.scrollTop = chatArea.scrollHeight;
}

/**
 * Show error message to user
 * @param {string} message - The error message to display
 */
function showError(message) {
    if (errorModal && errorMessage) {
        errorMessage.textContent = message;
        errorModal.classList.remove('hidden');
    } else {
        // Fallback to alert if modal not available
        alert(`Error: ${message}`);
    }
}

/**
 * Close error modal
 */
function closeErrorModal() {
    if (errorModal) {
        errorModal.classList.add('hidden');
    }
}

/**
 * Handle network errors and display appropriate messages
 * @param {Error} error - The error object
 */
function handleNetworkError(error) {
    console.error('Network error:', error);
    
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
        showError('Cannot connect to the server. Please check your internet connection.');
    } else if (error.message.includes('500')) {
        showError('Server error. The chat service may be temporarily unavailable.');
    } else if (error.message.includes('503')) {
        showError('The AI service is temporarily unavailable. Please try again later.');
    } else {
        showError('An unexpected error occurred. Please try again.');
    }
}

// Global error handler for unhandled promises
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    if (!isLoading) {
        handleNetworkError(event.reason);
    }
});

// Make closeErrorModal available globally for HTML onclick
window.closeErrorModal = closeErrorModal;