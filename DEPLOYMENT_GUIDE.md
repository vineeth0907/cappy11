# Cappy Deployment Guide

## Current Issue
Your Streamlit app is failing to deploy due to dependency installation errors.

## Solution Options

### Option 1: Use Simplified App (Recommended)
1. **Rename files:**
   ```bash
   mv app.py app-original.py
   mv app-simple.py app.py
   mv utils.py utils-original.py
   mv utils-simple.py utils.py
   ```

2. **Use minimal requirements:**
   ```bash
   mv requirements.txt requirements-full.txt
   mv requirements-basic.txt requirements.txt
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Simplify app for deployment - remove scikit-learn dependency"
   git push
   ```

### Option 2: Fix Original App Dependencies
If you prefer to keep the original functionality:

1. **Use conservative requirements:**
   ```bash
   mv requirements.txt requirements-current.txt
   mv requirements-conservative.txt requirements.txt
   ```

2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Fix dependencies with conservative versions"
   git push
   ```

## What Was Changed

### Simplified App (`app-simple.py`)
- ✅ Removed `scikit-learn` dependency
- ✅ Replaced TF-IDF with simple text matching
- ✅ Kept all core functionality
- ✅ Same UI and user experience

### Conservative Requirements
- ✅ Used exact versions instead of ranges
- ✅ Downgraded to more stable versions
- ✅ Removed problematic `grpcio` dependency

## Testing Locally

Before deploying, test locally:

```bash
# Install minimal requirements
pip install -r requirements-basic.txt

# Run simplified app
streamlit run app-simple.py
```

## Deployment Steps

1. **Choose your option above**
2. **Commit and push changes**
3. **Wait for Streamlit Cloud to redeploy**
4. **Check deployment logs for any remaining errors**

## If Still Failing

1. **Check Streamlit Cloud logs** for specific error messages
2. **Try the most minimal approach:**
   - Use only `streamlit` and `google-generativeai`
   - Remove all other dependencies temporarily
3. **Contact Streamlit support** if issues persist

## Rollback

If you want to restore the original app:
```bash
git checkout HEAD~1
git push --force
```

## Support
- Check Streamlit Cloud logs for specific error details
- Verify your repository has the correct file structure
- Ensure your main app file is named `app.py` or `main.py`
