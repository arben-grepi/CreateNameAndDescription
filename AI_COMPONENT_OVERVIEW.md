# AI-Powered Product Content Generator - Technical Overview

## Architecture

The component is built as a **FastAPI microservice** that uses **Large Language Model (LLM) technology** to transform product data into optimized display content. The service acts as a REST API backend that can be integrated with frontend applications.

### Technology Stack

- **Backend Framework**: FastAPI (Python) - provides REST API endpoints with automatic OpenAPI documentation
- **AI Framework**: LangChain - orchestrates LLM interactions, prompt management, and output parsing
- **AI Model**: Anthropic Claude (Haiku variant) - performs the content generation
- **Output Format**: Structured JSON using Pydantic models for type safety and validation

## AI Techniques and Implementation

### 1. Prompt Engineering

The system employs **multi-layered prompt engineering** to guide the LLM's behavior:

- **System Instructions**: High-level role definition and behavioral guidelines
- **Structured Instructions**: Detailed, hierarchical instructions that define:
  - Output format requirements (display name, description, bullet points)
  - Content length and style constraints
  - Compliance and safety guidelines
  - Accuracy requirements and constraints
- **Context Injection**: Product data (title and body HTML) is injected into the prompt as context
- **Format Instructions**: JSON schema instructions generated from Pydantic models to ensure structured output

The prompt template uses a **few-shot approach** with embedded examples and constraints rather than explicit examples, relying on detailed instruction sets to guide behavior.

### 2. Structured Output Parsing

The system uses **Pydantic Output Parsers** from LangChain to ensure type-safe, validated responses:

- **Schema Definition**: Pydantic models define the expected output structure with field descriptions and constraints
- **Automatic Parsing**: LangChain's parser converts LLM text responses into structured Python objects
- **Validation**: Pydantic validates the parsed output against the schema, catching malformed responses
- **Error Handling**: Invalid outputs trigger exceptions that are caught and returned as HTTP errors

This technique eliminates the need for manual JSON parsing and provides runtime type safety.

### 3. LLM Orchestration with LangChain

The system uses **LangChain's chain composition** pattern:

- **Prompt Template**: Defines the message structure with placeholders for dynamic content
- **Partial Prompting**: Instructions and format schemas are pre-baked into the prompt template
- **Chain Pipeline**: `prompt | llm | parser` creates a sequential processing pipeline
- **Invocation**: The chain is invoked with product data, which flows through prompt → LLM → parser → validated output

This abstraction simplifies LLM interaction and provides a clean separation between prompt design, model invocation, and output processing.

### 4. Constraint-Based Generation

The AI is constrained through multiple mechanisms:

- **Instruction Constraints**: Explicit rules in the prompt (e.g., "MUST be shorter than original title")
- **Schema Constraints**: Pydantic field validators enforce length limits and data types
- **Compliance Constraints**: Built-in guidelines to avoid health claims and platform violations
- **Accuracy Constraints**: Instructions to never invent information not present in input

These constraints work together to ensure the generated content meets specific requirements while maintaining safety and accuracy.

### 5. Context-Aware Processing

The LLM performs several processing tasks:

- **Information Extraction**: Parses HTML content to identify relevant specifications and features
- **Content Distillation**: Removes unnecessary words, brand names, and technical codes from titles
- **Semantic Understanding**: Identifies core product benefits and key features from unstructured data
- **Content Reformulation**: Transforms technical or poorly formatted data into customer-friendly language
- **Selective Generation**: Decides whether to generate bullet points based on available information quality

## Deployment and Production

### Containerization

The service is containerized using **Docker**:

- **Base Image**: Python 3.12 slim image for minimal footprint
- **Dependency Management**: Requirements are installed in a separate layer for better caching
- **Port Configuration**: Uses environment variable `PORT` (defaults to 8080) for cloud platform compatibility
- **Runtime**: Uvicorn ASGI server runs the FastAPI application

### Production Platform: Google Cloud Run

The service is deployed to **Google Cloud Run**, a serverless container platform:

- **Deployment Method**: Source-based deployment using Cloud Build
- **Build Process**: Cloud Build automatically builds the Docker image from source code
- **Container Registry**: Images are stored in Google Container Registry (GCR)
- **Service Configuration**: Managed platform with automatic scaling and load balancing
- **Region**: Deployed to specific regions (e.g., `us-central1`, `europe-west4`)

### Deployment Configuration

The deployment uses several configuration files:

- **Dockerfile**: Defines the container image build process
- **cloudbuild.yaml**: Cloud Build configuration for automated CI/CD pipelines
- **app.yaml**: Alternative App Engine configuration (if using App Engine instead of Cloud Run)
- **backend.yaml**: Firebase Backend Apps configuration (if using Firebase hosting)

### Build and Deploy Pipeline

The deployment pipeline follows these steps:

1. **Source Push**: Code is pushed to the repository
2. **Cloud Build Trigger**: Automatically builds Docker image using the Dockerfile
3. **Image Push**: Built image is pushed to Google Container Registry
4. **Cloud Run Deploy**: New revision is deployed to Cloud Run service
5. **Traffic Routing**: Cloud Run automatically routes traffic to the new revision

## Permissions and Security Configuration

### CORS (Cross-Origin Resource Sharing)

The service implements **CORS middleware** to control access from frontend applications:

- **Configuration**: CORS origins are configurable via environment variable `CORS_ORIGINS`
- **Format**: Comma-separated list of allowed origins (e.g., `https://yourdomain.com,https://app.yourdomain.com`)
- **Default**: Falls back to localhost origins for development
- **Middleware**: FastAPI CORS middleware allows specified origins, credentials, methods, and headers

This ensures that only authorized frontend applications can make requests to the API.

### API Key Management

The Anthropic API key is managed securely:

- **Storage**: Production uses **Google Secret Manager** instead of environment variables
- **Secret Creation**: API key is stored as a secret in Secret Manager
- **Access Control**: Cloud Run service account is granted `roles/secretmanager.secretAccessor` role
- **Injection**: Secret is injected at runtime via `--set-secrets` flag during deployment
- **Rotation**: Secrets can be rotated without redeploying the service

### IAM (Identity and Access Management)

Google Cloud IAM roles are configured for:

- **Service Account**: Cloud Run uses a compute service account
- **Secret Access**: Service account has permission to read from Secret Manager
- **Public Access**: Service is deployed with `--allow-unauthenticated` flag, making it publicly accessible
- **Alternative**: Can be configured to require authentication if needed

### Environment Variables

Configuration is managed through environment variables:

- **ANTHROPIC_API_KEY**: Required - stored in Secret Manager for production
- **CORS_ORIGINS**: Optional - comma-separated list of allowed origins
- **PORT**: Automatically set by Cloud Run (defaults to 8080 in Dockerfile)

### Security Best Practices

The deployment follows security best practices:

- **Secret Management**: Sensitive credentials are stored in Secret Manager, not in code or environment variables
- **Least Privilege**: Service account has minimal required permissions
- **CORS Restrictions**: Only specified origins can access the API
- **Container Security**: Minimal base image reduces attack surface
- **No Hardcoded Secrets**: All sensitive data is externalized to configuration

## API Structure

### Endpoints

- **GET /** - Health check endpoint that returns service status
- **POST /generate** - Main endpoint that accepts product data and returns generated content

### Request/Response Format

- **Request**: JSON body with `title` (string) and `body_html` (string) fields
- **Response**: JSON object with `displayName`, `displayDescription`, and `bulletpoints` fields
- **Validation**: Both request and response are validated using Pydantic models
- **Error Handling**: HTTP exceptions with descriptive error messages for failures

## AI Skills

LangChain, Anthropic Claude API, Prompt Engineering, Structured Output Parsing, LLM Orchestration, Pydantic Models, Type-Safe AI Responses, Constraint-Based Generation, Context-Aware Processing, Compliance & Safety Guidelines, Error Handling for LLM Systems, FastAPI, Python, JSON Schema Validation, Production AI Deployment, Docker, Google Cloud Run, Secret Manager, IAM Configuration
