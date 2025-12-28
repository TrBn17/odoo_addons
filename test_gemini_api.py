#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

print("=" * 60)
print("TESTING GEMINI API CONNECTION")
print("=" * 60)

# Check API Key
api_key = os.getenv('GEMINI_API_KEY')
print(f"\n1. Checking API Key...")
if not api_key:
    print("   ❌ GEMINI_API_KEY not found in environment!")
    sys.exit(1)
else:
    print(f"   ✅ API Key found: {api_key[:10]}...{api_key[-4:]}")

# Try to import library
print(f"\n2. Importing google.generativeai...")
try:
    import google.generativeai as genai
    print("   ✅ Library imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import: {e}")
    sys.exit(1)

# Configure API
print(f"\n3. Configuring Gemini API...")
try:
    genai.configure(api_key=api_key)
    print("   ✅ API configured")
except Exception as e:
    print(f"   ❌ Configuration failed: {e}")
    sys.exit(1)

# List available models
print(f"\n4. Listing available models...")
try:
    models = genai.list_models()
    print("   ✅ Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"      • {model.name}")
except Exception as e:
    print(f"   ❌ Failed to list models: {e}")
    sys.exit(1)

# Test with a simple prompt
print(f"\n5. Testing with a simple prompt...")
try:
    # Try the model that should work
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello in Vietnamese")
    print(f"   ✅ Test successful!")
    print(f"   Response: {response.text[:100]}...")
except Exception as e:
    print(f"   ❌ Test failed: {e}")
    print(f"\n   Trying alternative model names...")
    
    # Try alternative models
    for model_name in ['models/gemini-pro', 'gemini-1.5-pro', 'models/gemini-1.5-pro']:
        try:
            print(f"      Testing {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"      ✅ {model_name} works!")
            print(f"      Response: {response.text[:50]}...")
            break
        except Exception as e2:
            print(f"      ❌ {model_name} failed: {e2}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
