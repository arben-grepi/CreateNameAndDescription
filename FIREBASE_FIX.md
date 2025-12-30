# Firebase Backend Apps - Fixing Python Detection

## The Problem

Firebase App Hosting is trying to auto-detect your app and defaulting to Node.js buildpacks instead of using Docker for Python.

## The Solution

Firebase Backend Apps **DOES support Python via Docker**, but you need to ensure:

1. **Dockerfile exists** in the root directory ✅ (we have this)
2. **No conflicting files** that trigger Node.js detection
3. **Explicit Docker configuration** in Firebase Console

## Quick Fix - Deploy via Cloud Run Directly

Since Firebase Backend Apps uses Cloud Run under the hood, you can deploy directly:

```bash
# Set your project
gcloud config set project ecom-store-generator-41064

# Deploy to Cloud Run (same region as your Firebase app)
gcloud run deploy create-name-description \
  --source . \
  --platform managed \
  --region europe-west4 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here,CORS_ORIGINS=*
```

This will:
- Build using the Dockerfile (Python)
- Deploy to Cloud Run
- Give you a URL you can use in your Next.js app

## Alternative: Configure Firebase to Use Docker

If you want to use Firebase Backend Apps UI:

1. **In Firebase Console** → Backend Apps → Your App
2. **Go to Settings** → Build Configuration
3. **Select**: "Use Dockerfile" or "Custom Build"
4. **Dockerfile path**: `Dockerfile`
5. **Build context**: `.` (root)

## Files Created

- ✅ `Dockerfile` - Python container definition
- ✅ `.dockerignore` - Excludes unnecessary files
- ✅ `.gcloudignore` - Excludes files from gcloud upload
- ✅ `procfile` - Alternative entry point (if needed)
- ✅ `backend.yaml` - Firebase Backend Apps config

## Verify Dockerfile Works Locally

Test the Dockerfile before deploying:

```bash
# Build locally
docker build -t product-content-api .

# Run locally
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=your_key product-content-api

# Test
curl http://localhost:8080/
```

If this works, the deployment should work too.

## Recommended Approach

**Use Cloud Run directly** (it's what Firebase Backend Apps uses anyway):

```bash
gcloud run deploy create-name-description \
  --source . \
  --platform managed \
  --region europe-west4 \
  --allow-unauthenticated \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:latest \
  --set-env-vars CORS_ORIGINS=*
```

Then update your Next.js app to use the Cloud Run URL instead of the Firebase Backend Apps URL.

