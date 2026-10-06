"""
Property-based tests for SimpleGroqChat
Demonstrates Kiro Lesson 4: Property-based Testing

These tests verify key properties of the chatbot system:
1. Valid messages always produce responses
2. API errors return valid JSON with error fields  
3. Empty/whitespace messages are rejected
"""

import json
import pytest
from hypothesis import given, strategies as st, settings, example
from app import app


class TestChatProperties:
    """Property-based tests for chat functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test client"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    @given(st.text(min_size=1, max_size=100).filter(lambda x: x.strip()))
    @settings(max_examples=20, deadline=5000)
    @example("Hello")
    @example("How are you?")
    @example("What is 2+2?")
    def test_valid_messages_get_responses(self, message):
        """
        Property: Valid non-empty messages should always get a response
        
        This test verifies that any non-empty message produces either:
        - A successful response with 'response' field
        - An error response with 'error' field
        
        But never crashes or returns invalid JSON.
        """
        # Send message to chat endpoint
        response = self.client.post('/api/chat', 
                                  json={'message': message},
                                  content_type='application/json')
        
        # Response should be valid JSON
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        
        # Should get either success or error response
        if response.status_code == 200:
            # Success case - should have response field
            assert 'response' in data
            assert isinstance(data['response'], str)
            assert len(data['response'].strip()) > 0  # Non-empty response
            
        else:
            # Error case - should have error field
            assert 'error' in data
            assert isinstance(data['error'], str)
            assert len(data['error'].strip()) > 0  # Non-empty error message
            
        # Should never have both response and error
        assert not ('response' in data and 'error' in data)
    
    @given(st.one_of(
        st.just(""),           # Empty string
        st.just("   "),        # Whitespace only
        st.just("\n\t  \n"),   # Mixed whitespace
        st.text(max_size=0),   # Zero-length text
    ))
    @settings(max_examples=10)
    def test_empty_messages_rejected(self, empty_message):
        """
        Property: Empty or whitespace-only messages should be rejected
        
        This verifies input validation works correctly.
        """
        response = self.client.post('/api/chat',
                                  json={'message': empty_message},
                                  content_type='application/json')
        
        # Should return 400 Bad Request
        assert response.status_code == 400
        
        # Should return valid JSON with error
        data = json.loads(response.data)
        assert 'error' in data
        assert isinstance(data['error'], str)
        assert 'empty' in data['error'].lower() or 'required' in data['error'].lower()
    
    @given(st.one_of(
        st.none(),                    # No message field
        st.integers(),                # Wrong type
        st.lists(st.text()),         # Wrong type
        st.dictionaries(st.text(), st.text())  # Wrong type
    ))
    @settings(max_examples=10)
    def test_invalid_message_types_rejected(self, invalid_message):
        """
        Property: Invalid message types should be handled gracefully
        
        This tests robustness against malformed requests.
        """
        # Create request with invalid message
        if invalid_message is None:
            request_data = {}  # Missing message field
        else:
            request_data = {'message': invalid_message}
            
        response = self.client.post('/api/chat',
                                  json=request_data,
                                  content_type='application/json')
        
        # Should return 400 Bad Request for invalid input
        assert response.status_code == 400
        
        # Should return valid JSON with error
        data = json.loads(response.data)
        assert 'error' in data
        assert isinstance(data['error'], str)
    
    def test_api_error_responses_are_valid_json(self):
        """
        Property: API error responses should always return valid JSON
        
        This tests error handling when API is unavailable.
        """
        # Test with missing API key (simulated by temporarily clearing it)
        import os
        original_key = os.environ.get('GROQ_API_KEY')
        
        # Temporarily remove API key
        if 'GROQ_API_KEY' in os.environ:
            del os.environ['GROQ_API_KEY']
        
        try:
            # Restart app without API key
            from importlib import reload
            import app as app_module
            reload(app_module)
            
            client = app_module.app.test_client()
            
            response = client.post('/api/chat',
                                 json={'message': 'Test message'},
                                 content_type='application/json')
            
            # Should return 500 Internal Server Error
            assert response.status_code == 500
            
            # Should return valid JSON with error
            data = json.loads(response.data)
            assert 'error' in data
            assert isinstance(data['error'], str)
            
        finally:
            # Restore API key if it existed
            if original_key:
                os.environ['GROQ_API_KEY'] = original_key
    
    @given(st.text(min_size=1001, max_size=2000))
    @settings(max_examples=5)
    def test_long_messages_handled_gracefully(self, long_message):
        """
        Property: Very long messages should be handled gracefully
        
        This tests system behavior with edge case inputs.
        """
        response = self.client.post('/api/chat',
                                  json={'message': long_message},
                                  content_type='application/json')
        
        # Should return valid JSON (either success or error)
        data = json.loads(response.data)
        
        # Should have either response or error field
        assert 'response' in data or 'error' in data
        
        # If error, should be meaningful
        if 'error' in data:
            assert isinstance(data['error'], str)
            assert len(data['error']) > 0


def test_chat_endpoint_exists():
    """Basic test to verify the chat endpoint is available"""
    with app.test_client() as client:
        # Test that endpoint exists (even if it returns an error)
        response = client.post('/api/chat',
                             json={'message': 'test'},
                             content_type='application/json')
        
        # Should not return 404
        assert response.status_code != 404


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v'])