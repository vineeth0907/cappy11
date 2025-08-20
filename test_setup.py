#!/usr/bin/env python3
"""
Test script to verify Cappy setup
Run this to check if all dependencies are working correctly
"""

def test_imports():
    """Test if all required packages can be imported."""
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True

def test_utils():
    """Test if utils.py can be imported and functions work."""
    try:
        from utils import load_company_data, create_contextual_prompt
        print("✅ Utils module imported successfully")
        
        # Test company data loading
        company_data = load_company_data()
        if company_data and len(company_data) > 100:
            print("✅ Company data loaded successfully")
        else:
            print("❌ Company data loading failed or data too short")
            return False
        
        # Test prompt creation
        prompt = create_contextual_prompt("What services does Capserve offer?", company_data)
        if prompt and "Capserve" in prompt:
            print("✅ Prompt creation working")
        else:
            print("❌ Prompt creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist."""
    import os
    
    required_files = [
        "app.py",
        "utils.py", 
        "requirements.txt",
        "README.md",
        "data/capserve_info.txt"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Testing Cappy Setup...\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("Utils Module", test_utils)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"📋 Testing {test_name}...")
        if test_func():
            print(f"✅ {test_name} passed\n")
        else:
            print(f"❌ {test_name} failed\n")
            all_passed = False
    
    if all_passed:
        print("🎉 All tests passed! Cappy is ready to run.")
        print("\n🚀 Next steps:")
        print("1. Create a .env file with your GOOGLE_API_KEY")
        print("2. Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Try running: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
