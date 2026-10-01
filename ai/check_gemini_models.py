"""
Quick script to list available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("📋 Available Gemini Models:\n")
print("-" * 70)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Description: {model.description}")
        print(f"   Methods: {', '.join(model.supported_generation_methods)}")
        print("-" * 70)
