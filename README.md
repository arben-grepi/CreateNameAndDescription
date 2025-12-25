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

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions for:
- Firebase Functions
- Cloud Run
- Railway
- Render

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
