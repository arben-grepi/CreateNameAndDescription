# Firebase Backend Apps - Python Deployment

## Problem

Firebase App Hosting is trying to auto-detect your app as Node.js and using buildpacks, but this is a Python app. We need to force Docker usage.

## Solution

Firebase Backend Apps supports Python via Docker. The `backend.yaml` and `Dockerfile` files have been created to configure this.

## Deployment Steps

### Option 1: Using Firebase Console

1. **Go to Firebase Console** → Backend Apps
2. **Create/Edit your backend app**
3. **Set Build Configuration:**
   - Build type: **Docker**
   - Dockerfile path: `Dockerfile`
   - Build context: `.` (root directory)

4. **Set Environment Variables:**
   - `ANTHROPIC_API_KEY` - Your Anthropic API key (use Secret Manager)
   - `CORS_ORIGINS` - Comma-separated origins (e.g., `https://yourdomain.com`)

5. **Deploy**

### Option 2: Using Firebase CLI

1. **Install Firebase CLI** (if not already):
   ```bash
   npm install -g firebase-tools
   ```

2. **Login and initialize:**
   ```bash
   firebase login
   firebase init backend
   ```

3. **Deploy:**
   ```bash
   firebase deploy --only backend
   ```

### Option 3: Manual Docker Build (if auto-detection fails)

If Firebase still tries to use buildpacks, you can build and push the Docker image manually:

1. **Build the Docker image:**
   ```bash
   docker build -t gcr.io/PROJECT_ID/product-content-api:latest .
   ```

2. **Push to Google Container Registry:**
   ```bash
   docker push gcr.io/PROJECT_ID/product-content-api:latest
   ```

3. **Deploy to Cloud Run (which Firebase Backend Apps uses):**
   ```bash
   gcloud run deploy product-content-api \
     --image gcr.io/PROJECT_ID/product-content-api:latest \
     --platform managed \
     --region europe-west4 \
     --allow-unauthenticated \
     --set-env-vars ANTHROPIC_API_KEY=your_key,CORS_ORIGINS=*
   ```

## Configuration Files

### `backend.yaml`
This file tells Firebase to use Docker and Python runtime.

### `Dockerfile`
This builds the Python container with all dependencies.

### Environment Variables

Set these in Firebase Console → Backend Apps → Your App → Environment Variables:

- **ANTHROPIC_API_KEY** (required) - Use Secret Manager for this
- **CORS_ORIGINS** (optional) - Defaults to `*` if not set

## Troubleshooting

### If buildpack detection still fails:

1. **Check Dockerfile exists** in root directory
2. **Verify backend.yaml** is present
3. **Try explicit Docker build** (Option 3 above)

### If deployment succeeds but app doesn't work:

1. **Check logs:**
   - Firebase Console → Backend Apps → Your App → Logs
   - Look for Python errors or import issues

2. **Test health endpoint:**
   ```bash
   curl https://your-backend-url.hosted.app/
   ```

3. **Verify environment variables:**
   - Ensure `ANTHROPIC_API_KEY` is set correctly
   - Check Secret Manager permissions

### Common Issues:

- **Port binding**: The app uses `PORT` env var (defaults to 8080)
- **CORS errors**: Make sure `CORS_ORIGINS` includes your Next.js domain
- **Import errors**: All dependencies must be in `requirements.txt`

## Alternative: Use Cloud Run Directly

If Firebase Backend Apps continues to have issues, you can deploy directly to Cloud Run (which Firebase Backend Apps uses under the hood):

```bash
gcloud run deploy product-content-api \
  --source . \
  --platform managed \
  --region europe-west4 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key,CORS_ORIGINS=*
```

Then use the Cloud Run URL in your Next.js app instead of the Firebase Backend Apps URL.

