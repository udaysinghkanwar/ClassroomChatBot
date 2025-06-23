#!/usr/bin/env python3
"""
Test script for deployment configuration

This script tests the OAuth configuration and basic functionality
before deployment.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test that required environment variables are set."""
    print("🔍 Testing environment variables...")
    
    required_vars = [
        'GOOGLE_CLIENT_SECRETS_JSON',
        'OAUTH_REDIRECT_URI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_oauth_config():
    """Test OAuth configuration parsing."""
    print("\n🔍 Testing OAuth configuration...")
    
    try:
        client_secrets_json = os.getenv('GOOGLE_CLIENT_SECRETS_JSON')
        if not client_secrets_json:
            print("❌ GOOGLE_CLIENT_SECRETS_JSON not set")
            return False
        
        # Parse the JSON
        client_secrets = json.loads(client_secrets_json)
        
        # Check required fields
        required_fields = ['web', 'client_id', 'client_secret', 'redirect_uris']
        web_config = client_secrets.get('web', {})
        
        missing_fields = []
        for field in required_fields:
            if field not in web_config:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing OAuth fields: {missing_fields}")
            return False
        
        print("✅ OAuth configuration is valid")
        print(f"   Client ID: {web_config['client_id'][:10]}...")
        print(f"   Redirect URIs: {web_config['redirect_uris']}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in GOOGLE_CLIENT_SECRETS_JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing OAuth config: {e}")
        return False

def test_imports():
    """Test that all required modules can be imported."""
    print("\n🔍 Testing imports...")
    
    try:
        # Test OAuth web config
        from oauth_web_config import get_oauth_flow, get_user_credentials
        print("✅ oauth_web_config imports successfully")
        
        # Test Streamlit app
        import streamlit as st
        print("✅ streamlit imports successfully")
        
        # Test Google APIs
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        print("✅ Google API modules import successfully")
        
        # Test ADK
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        print("✅ ADK modules import successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing imports: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'streamlit_app.py',
        'oauth_web_config.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'system_root_agent/agent.py',
        'system_root_agent/subagents/announcement_agent/tools.py',
        'system_root_agent/subagents/course_work_agent/tools.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def main():
    """Run all tests."""
    print("🚀 LearnBridge Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_oauth_config,
        test_imports,
        test_file_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment configuration is ready.")
        print("\n📋 Next steps:")
        print("1. Update your OAuth client to 'Web application' type")
        print("2. Add redirect URIs to your Google Cloud Console")
        print("3. Deploy to Streamlit Cloud")
        print("4. Set environment variables in Streamlit Cloud")
    else:
        print("❌ Some tests failed. Please fix the issues above before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 