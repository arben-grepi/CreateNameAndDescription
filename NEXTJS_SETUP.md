# Next.js Setup - Update for Production

## Your Deployed API URL

**Production API:** `https://create-name-description-398748178376.europe-west4.run.app`

## What Changed

Your Next.js app already works. You just need to update the API URL.

## Update Your Environment Variable

In your Next.js `.env.local` file, change:

**Before (localhost):**
```env
NEXT_PUBLIC_PRODUCT_API_URL=http://localhost:8000
```

**After (production):**
```env
NEXT_PUBLIC_PRODUCT_API_URL=https://create-name-description-398748178376.europe-west4.run.app
```

## If Using Firebase App Hosting Secret Manager

1. Go to [Google Cloud Secret Manager](https://console.cloud.google.com/security/secret-manager?project=ecom-store-generator-41064)
2. Create/update secret: `NEXT_PUBLIC_PRODUCT_API_URL`
3. Value: `https://create-name-description-398748178376.europe-west4.run.app`
4. Ensure it's referenced in your `apphosting.yaml`

## That's It

Your existing code will automatically use the new URL. No code changes needed - just update the environment variable.

## Test It

```bash
curl https://create-name-description-398748178376.europe-west4.run.app/
```

You should see:
```json
{
  "message": "Product Content Generator API",
  "status": "running",
  ...
}
```
