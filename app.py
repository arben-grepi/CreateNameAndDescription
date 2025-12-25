"""
FastAPI server for generating product display content from Shopify data.

Run with: uvicorn app:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Product Content Generator API",
    description="Generate optimized product display content from Shopify product data",
    version="1.0.0"
)

# Enable CORS for Next.js app
# Allow origins from environment variable or default to localhost
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
cors_origins_list = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ProductContent model (same as in extract-shopify-features.py)
class ProductContent(BaseModel):
    """
    Generated product content for storefront display.
    """
    displayName: str = Field(
        ...,
        description="Short, catchy product name optimized for product cards. Must be shorter than the original title. Should be 3-8 words, remove unnecessary words like 'Brand Name:', 'SPECIFICATIONS', etc. Focus on the core product benefit or key feature."
    )
    
    displayDescription: str = Field(
        ...,
        description="Compelling product description in 2-4 sentences. Should highlight key benefits, target audience, and main use cases. Write in a natural, marketing-friendly tone. Remove technical jargon unless necessary. Should be 50-150 words."
    )
    
    bulletpoints: Optional[List[str]] = Field(
        default=None,
        max_length=5,
        description="Key features, benefits, or specifications as bullet points. Only include if there is relevant, valuable information in the body_html. Each bullet should be concise (5-15 words). Focus on unique selling points, key ingredients, benefits, or important specifications. If body_html doesn't contain useful information, return empty list or null."
    )


# Request model for the API endpoint
class ProductRequest(BaseModel):
    title: str = Field(..., description="Product title from Shopify")
    body_html: str = Field(..., description="Product description HTML (truncated at 'src=' to exclude images)")


# LLM Instructions
LLM_INSTRUCTIONS = """
You are an expert e-commerce copywriter specializing in product descriptions for online stores.

Your task is to generate optimized product content from Shopify product data:

INPUT:
- title: The original product title (may be long or contain unnecessary words)
- body_html: Product description HTML content (may contain specifications, features, etc.)

OUTPUT REQUIREMENTS:

1. displayName:
   - MUST be shorter than the original title
   - Should be 3-8 words
   - Remove unnecessary words like brand names, "SPECIFICATIONS", technical codes
   - Focus on the core product benefit or key feature
   - Make it catchy and memorable
   - Example: "Turmeric & Vitamin C Cream" instead of "Turmeric & Vitamin C Cream -Lightweight Nourishment for Face& Neck, Fast-Absorbing HydrationAll Skin Types"

2. displayDescription:
   - Write 2-4 compelling sentences (50-150 words)
   - Highlight key benefits and target audience
   - Use natural, marketing-friendly language
   - Remove technical jargon unless essential
   - Focus on what the product does and who it's for
   - Make it engaging and persuasive

3. bulletpoints:
   - Extract ONLY if body_html contains relevant, valuable information
   - Maximum 5 bullet points
   - Each bullet should be 5-15 words
   - Focus on:
     * Key ingredients or components
     * Unique selling points
     * Important benefits
     * Notable specifications (if relevant to purchase decision)
   - If body_html only contains generic info or no useful details, return empty list []
   - Each bullet should start with a capital letter and end without punctuation (unless it's a question)

GUIDELINES:
- Remove HTML tags and formatting from body_html when extracting information
- Don't include obvious information (e.g., "Suitable for all skin types" if it's a skincare product)
- Prioritize information that helps customers make purchase decisions
- Keep language natural and avoid robotic lists
- If the body_html is mostly empty or just contains basic specs, focus on creating a good description from the title

Return the data in the ProductContent BaseModel format.
"""


# Initialize LangChain components
llm = ChatAnthropic(model="claude-3-haiku-20240307")
parser = PydanticOutputParser(pydantic_object=ProductContent)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert e-commerce copywriter. Format your response as JSON."),
    ("human", "{instructions}\n\nPRODUCT DATA:\nTitle: {title}\nBody HTML: {body_html}\n\n{format_instructions}")
])

# Partial the prompt with instructions and format_instructions
prompt = prompt.partial(
    instructions=LLM_INSTRUCTIONS,
    format_instructions=parser.get_format_instructions()
)

# Create the chain
chain = prompt | llm | parser


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Product Content Generator API",
        "status": "running",
        "endpoints": {
            "generate": "/generate (POST)",
            "health": "/ (GET)"
        }
    }


@app.post("/generate", response_model=ProductContent)
async def generate_product_content(request: ProductRequest):
    """
    Generate optimized product display content from Shopify product data.
    
    Args:
        request: ProductRequest containing title and body_html
    
    Returns:
        ProductContent with displayName, displayDescription, and bulletpoints
    """
    try:
        # Invoke the LangChain chain
        result = chain.invoke({
            "title": request.title,
            "body_html": request.body_html
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating product content: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

