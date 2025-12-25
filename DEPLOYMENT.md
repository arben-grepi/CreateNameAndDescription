# Deployment Guide

## Firebase Functions Deployment

This FastAPI app can be deployed to Firebase Functions to serve as a backend for your Next.js app.

### Prerequisites

1. Firebase CLI installed: `npm install -g firebase-tools`
2. Firebase project set up
3. Python 3.9+ installed

### Setup Steps

1. **Initialize Firebase Functions (if not already done):**
   ```bash
   firebase init functions
   ```
   - Select Python as the language
   - Choose your Firebase project

2. **Copy files to Firebase Functions directory:**
   ```bash
   cp app.py functions/
   cp requirements.txt functions/
   ```

3. **Update `functions/main.py` (Firebase Functions entry point):**
   ```python
   from firebase_functions import https_fn
   from firebase_admin import initialize_app
   import app

   initialize_app()

   # Export the FastAPI app as a Firebase Function
   product_content_api = https_fn.on_request(
       cors=https_fn.CorsOptions(
           cors_origins=["*"],  # Configure as needed
           cors_methods=["GET", "POST"],
       ),
       timeout_sec=540,
       memory=512,
   )(app.app)
   ```

4. **Update `functions/requirements.txt`:**
   ```txt
   fastapi
   uvicorn[standard]
   python-dotenv
   pydantic
   langchain-anthropic
   langchain-core
   firebase-functions
   firebase-admin
   ```

5. **Set environment variables in Firebase:**
   ```bash
   firebase functions:config:set anthropic.api_key="your_api_key_here"
   ```

   Or use Firebase Functions environment config:
   ```bash
   firebase functions:secrets:set ANTHROPIC_API_KEY
   ```

6. **Deploy:**
   ```bash
   firebase deploy --only functions
   ```

## Alternative: Cloud Run / Railway / Render

### Environment Variables Required:
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `CORS_ORIGINS` (optional) - Comma-separated list of allowed origins

### Example Deployment Commands:

**Cloud Run:**
```bash
gcloud run deploy product-content-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars ANTHROPIC_API_KEY=your_key,CORS_ORIGINS=https://yourdomain.com
```

**Railway:**
1. Connect your GitHub repo
2. Set environment variables in Railway dashboard
3. Deploy automatically

**Render:**
1. Create new Web Service
2. Connect GitHub repo
3. Set environment variables
4. Build command: `pip install -r requirements.txt && uvicorn app:app --host 0.0.0.0 --port $PORT`

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   Create `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   CORS_ORIGINS=http://localhost:3000
   ```

3. **Run the server:**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

## Updating Your Next.js App

After deployment, update your `productContentApi.ts`:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_PRODUCT_API_URL || 
  'https://your-firebase-function-url.cloudfunctions.net/product_content_api';
```

