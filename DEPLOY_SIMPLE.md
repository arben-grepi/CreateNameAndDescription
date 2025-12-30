# Simple Deployment Guide - Recommended Approach

## Best Option: Deploy to Cloud Run Directly

This is the **easiest, most reliable, and conventional** approach. Cloud Run is what Firebase Backend Apps uses anyway, so you're just cutting out the middle layer.

## One-Command Deployment

```bash
# Set your project (if not already set)
gcloud config set project ecom-store-generator-41064

# Deploy (this builds from Dockerfile automatically)
gcloud run deploy create-name-description \
  --source . \
  --platform managed \
  --region europe-west4 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here,CORS_ORIGINS=*
```

That's it! 🎉

## Why This is Best

✅ **Simple** - One command, no configuration files needed  
✅ **Reliable** - Uses your Dockerfile directly, no buildpack detection issues  
✅ **Fast** - Builds and deploys in ~2-3 minutes  
✅ **Conventional** - Standard Google Cloud approach  
✅ **Same Infrastructure** - Cloud Run is what Firebase Backend Apps uses anyway  
✅ **Easy Updates** - Just run the same command again  

## After Deployment

You'll get a URL like:
```
https://create-name-description-xxxxx-ew.a.run.app
```

Use this URL in your Next.js app's `NEXT_PUBLIC_PRODUCT_API_URL` environment variable.

## Updating Your App

When you make changes, just run the same command again:
```bash
gcloud run deploy create-name-description --source . --region europe-west4 --allow-unauthenticated
```

## Using Secrets (Recommended for Production)

Instead of putting your API key in the command, use Secret Manager:

```bash
# Create secret (one time)
echo -n "your_anthropic_api_key" | gcloud secrets create anthropic-api-key --data-file=-

# Deploy with secret
gcloud run deploy create-name-description \
  --source . \
  --platform managed \
  --region europe-west4 \
  --allow-unauthenticated \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:latest \
  --set-env-vars CORS_ORIGINS=*
```

## That's It!

No need to mess with Firebase Backend Apps configuration, buildpack detection, or complex setup files. Just deploy directly to Cloud Run - it's the simplest path.

