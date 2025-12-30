# Secure Deployment - Using Secret Manager

## ⚠️ Important: Your API Key is Visible

If you've already deployed with the API key in the command, that's okay for testing, but for production you should use Secret Manager.

## Secure Deployment Steps

### Step 1: Create Secret (One Time)

```bash
# Create the secret (you'll be prompted to enter the key)
echo -n "YOUR_ANTHROPIC_API_KEY" | \
  gcloud secrets create anthropic-api-key --data-file=- --project=ecom-store-generator-41064
```

**Or set the project first:**
```bash
gcloud config set project ecom-store-generator-41064
echo -n "YOUR_ANTHROPIC_API_KEY" | \
  gcloud secrets create anthropic-api-key --data-file=-
```

### Step 2: Grant Cloud Run Access to the Secret

```bash
# Get your project number
PROJECT_NUMBER=$(gcloud projects describe ecom-store-generator-41064 --format="value(projectNumber)")

# Grant access
gcloud secrets add-iam-policy-binding anthropic-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=ecom-store-generator-41064
```

### Step 3: Deploy with Secret (No API Key in Command)

```bash
gcloud run deploy create-name-description \
  --source . \
  --platform managed \
  --region europe-west4 \
  --allow-unauthenticated \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:latest \
  --set-env-vars CORS_ORIGINS=*
```

## Update Existing Deployment

If you already deployed with the API key visible, you can update it to use secrets:

```bash
# First create the secret (Step 1 above)
# Then update the service
gcloud run services update create-name-description \
  --region europe-west4 \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:latest \
  --update-env-vars CORS_ORIGINS=*
```

This removes the API key from environment variables and uses the secret instead.

## Benefits of Using Secrets

✅ API key not visible in command history  
✅ API key not visible in Cloud Run environment variables UI  
✅ Can rotate secrets without redeploying  
✅ Better security practices  
✅ Audit trail of secret access  

