# Product Content Generator API

A FastAPI server that generates optimized product display content from Shopify product data using LangChain and Claude AI.

## Features

- 🚀 FastAPI-based REST API
- 🤖 AI-powered content generation using Claude (Anthropic)
- 📦 Structured output with Pydantic models
- 🔒 Environment-based configuration
- 🌐 CORS support for Next.js integration

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Run Locally

```bash
uvicorn app:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## API Endpoints

### POST `/generate`

Generate optimized product content from Shopify product data.

**Request:**
```json
{
  "title": "Product title from Shopify",
  "body_html": "Product description HTML"
}
```

**Response:**
```json
{
  "displayName": "Short, catchy product name",
  "displayDescription": "Compelling product description...",
  "bulletpoints": ["Feature 1", "Feature 2"]
}
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variables
- `pydantic` - Data validation
- `langchain-anthropic` - Anthropic/Claude integration
- `langchain-core` - LangChain core functionality

## Deployment to Google Cloud Run

This service is published to **Google Cloud Run**, a serverless container platform. Here's how to deploy it:

### Prerequisites

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Authenticate: `gcloud auth login`
3. Set your project: `gcloud config set project YOUR_PROJECT_ID`
4. Enable required APIs:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   ```

### Quick Deploy

Deploy with a single command (builds from Dockerfile automatically):

```bash
gcloud run deploy product-content-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here,CORS_ORIGINS=https://yourdomain.com
```

After deployment, you'll receive a URL like:
```
https://product-content-api-xxxxx-uc.a.run.app
```

### Using Secret Manager (Recommended for Production)

For better security, store your API key in Google Secret Manager:

```bash
# Create secret (one time)
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

### Updating the Deployment

To update after making changes, simply run the deploy command again:
```bash
gcloud run deploy product-content-api --source . --region us-central1 --allow-unauthenticated
```

## Next.js Integration

Call the API from your Next.js app using `fetch()`:

```typescript
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title, body_html }),
});
const content = await response.json();
```

## License

MIT
