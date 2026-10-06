"""Direct test of Gemini API"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key (first 20 chars): {api_key[:20]}...")
print(f"API Key length: {len(api_key)}")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✓ Model initialized")
    
    response = model.generate_content("Say hello")
    print(f"✓ Response received: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
