# 🚀 LearnBridge Public Deployment Guide

This guide will help you deploy your Google Classroom chatbot publicly using Streamlit Cloud.

## 📋 Prerequisites

1. **Google Cloud Project** with Google Classroom API enabled
2. **OAuth 2.0 Web Application** credentials (not desktop app)
3. **GitHub repository** with your code
4. **Streamlit Cloud** account (free)

## 🔧 Step 1: Update Google Cloud OAuth Configuration

### 1.1 Change OAuth Client Type
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Credentials"
3. Find your OAuth 2.0 Client ID
4. Click "Edit" and change the application type from "Desktop application" to **"Web application"**
5. Add authorized redirect URIs:
   - `https://your-app-name.streamlit.app/oauth2callback`
   - `https://your-app-name.streamlit.app/`
6. Save the changes

### 1.2 Download Updated Credentials
1. Download the updated `client_secret.json` file
2. Open the file and copy the entire JSON content

## 🌐 Step 2: Deploy to Streamlit Cloud

### 2.1 Prepare Your Repository
1. Push all your code to GitHub
2. Make sure these files are in your repository:
   - `streamlit_app.py` (main app)
   - `oauth_web_config.py` (OAuth configuration)
   - `requirements.txt` (dependencies)
   - `.streamlit/config.toml` (Streamlit config)
   - All agent files in `system_root_agent/`

### 2.2 Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to: `streamlit_app.py`
6. Click "Deploy!"

### 2.3 Configure Environment Variables
In your Streamlit Cloud app settings, add these environment variables:

```bash
GOOGLE_CLIENT_SECRETS_JSON={"web":{"client_id":"your-client-id","project_id":"your-project-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"your-client-secret","redirect_uris":["https://your-app-name.streamlit.app/oauth2callback"]}}
OAUTH_REDIRECT_URI=https://your-app-name.streamlit.app/oauth2callback
```

**Important:** Replace the JSON with your actual `client_secret.json` content and update the redirect URI to match your app URL.

## 🔐 Step 3: Security Considerations

### 3.1 OAuth Scopes
Your app requests these scopes:
- `classroom.announcements.readonly` - Read announcements
- `classroom.courses.readonly` - Read course information
- `classroom.coursework.students.readonly` - Read coursework (teachers)
- `classroom.coursework.me.readonly` - Read coursework (students)
- `calendar.events` - Add events to Google Calendar

### 3.2 Data Privacy
- ✅ User credentials are stored only in browser session
- ✅ No permanent data storage on servers
- ✅ Each user authenticates with their own Google account
- ✅ Users can revoke access anytime

## 🧪 Step 4: Testing Your Deployment

### 4.1 Test Authentication Flow
1. Visit your deployed app URL
2. Click "Connect Google Classroom"
3. Complete the OAuth flow
4. Verify you can access your classroom data

### 4.2 Test Features
- 📢 Get announcements
- 📚 Get coursework/assignments
- 💬 Chat with the AI assistant
- 📅 Calendar integration (if implemented)

## 🚨 Troubleshooting

### Common Issues:

#### 1. "OAuth Error: redirect_uri_mismatch"
- **Solution**: Update the redirect URI in Google Cloud Console to match your app URL exactly

#### 2. "Failed to initialize Google Classroom API service"
- **Solution**: Check that `GOOGLE_CLIENT_SECRETS_JSON` environment variable is set correctly

#### 3. "No courses found"
- **Solution**: Ensure the user has access to Google Classroom courses and has completed the OAuth flow

#### 4. "Module not found" errors
- **Solution**: Check that all dependencies are in `requirements.txt` and the file paths are correct

### Debug Mode
To debug issues, you can temporarily enable debug mode by adding to your environment variables:
```bash
STREAMLIT_LOGGER_LEVEL=debug
```

## 📈 Step 5: Monitoring and Maintenance

### 5.1 Monitor Usage
- Check Streamlit Cloud dashboard for app performance
- Monitor Google Cloud Console for API usage
- Watch for any authentication errors

### 5.2 Regular Maintenance
- Keep dependencies updated
- Monitor Google API quotas
- Check for any security updates

## 🔄 Alternative Deployment Options

### Option 1: Railway
- Similar to Streamlit Cloud
- Good for Python web apps
- Automatic deployments from GitHub

### Option 2: Heroku
- More control over the environment
- Requires Procfile and runtime.txt
- Free tier discontinued

### Option 3: Vercel
- Good for static sites
- Limited Python support
- Not recommended for this app

## 🎉 Success!

Your Google Classroom chatbot is now publicly accessible! Users can:
1. Visit your app URL
2. Authenticate with their Google account
3. Access their classroom data through the AI assistant
4. Get personalized help with their coursework

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Streamlit Cloud logs
3. Verify Google Cloud Console settings
4. Test with a different Google account

---

**Remember**: This deployment is designed for individual users to access their own Google Classroom data. Each user must authenticate with their own Google account. 