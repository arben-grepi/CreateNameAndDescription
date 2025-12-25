# Google Cloud Run Deployment Guide

## Problem Fixed

The error you encountered was because Google Cloud Build was trying to auto-detect your project type and defaulted to Node.js buildpacks. This has been fixed by adding a `Dockerfile` which forces Docker-based deployment.

## Quick Deploy

### 1. Set up Google Cloud (if not done):
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable required APIs:
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### 3. Deploy to Cloud Run:
```bash
gcloud run deploy product-content-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here,CORS_ORIGINS=https://yourdomain.com
```

### 4. Set secrets (recommended for production):
```bash
# Create secret
echo -n "your_anthropic_api_key" | gcloud secrets create anthropic-api-key --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding anthropic-api-key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy product-content-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:latest \
  --set-env-vars CORS_ORIGINS=https://yourdomain.com
```

## Files Created

- **Dockerfile** - Defines the container image (forces Python detection)
- **.dockerignore** - Excludes unnecessary files from Docker build
- **cloudbuild.yaml** - Cloud Build configuration (optional)
- **app.yaml** - App Engine config (alternative deployment)

## Environment Variables

Set these in Cloud Run:
- `ANTHROPIC_API_KEY` - Required (use Secret Manager for production)
- `CORS_ORIGINS` - Optional, comma-separated list of allowed origins

## Verify Deployment

After deployment, you'll get a URL like:
```
https://product-content-api-xxxxx-uc.a.run.app
```

Test it:
```bash
curl https://product-content-api-xxxxx-uc.a.run.app/
```

## Troubleshooting

If you still get buildpack errors:
1. Make sure `Dockerfile` is in the root directory
2. Check that `.dockerignore` exists
3. Try deploying with explicit Docker build:
   ```bash
   docker build -t product-content-api .
   gcloud run deploy product-content-api --image product-content-api
   ```

