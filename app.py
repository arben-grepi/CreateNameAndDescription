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

CRITICAL: ACCURACY AND COMPLIANCE ARE MORE IMPORTANT THAN MARKETING FLARE.

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
   - ONLY use words from the title - do not add information not present
   - Example: "Turmeric & Vitamin C Cream" instead of "Turmeric & Vitamin C Cream -Lightweight Nourishment for Face& Neck, Fast-Absorbing HydrationAll Skin Types"

2. displayDescription:
   - Write 2-4 compelling sentences (50-150 words)
   - ONLY describe what is explicitly stated in the title and body_html
   - If body_html is minimal or empty, work with what you have from the title
   - Do NOT invent features, benefits, or specifications that are not mentioned
   - If there's limited information, write a shorter but accurate description
   - Accuracy is more important than having a long description
   - Use natural, marketing-friendly language based on available information
   - If input lacks usable info, it's acceptable to have a shorter description

3. bulletpoints:
   - ONLY include bullet points if body_html contains specific, extractable information
   - DO NOT create bullet points from generic or obvious information
   - DO NOT invent bullet points if body_html is empty or lacks detail
   - If body_html has no useful information, return null or empty list []
   - Maximum 5 bullet points, but only if you have 5 distinct pieces of information
   - If you only have 2 pieces of information, only create 2 bullet points
   - It's better to have fewer accurate bullet points than to make up information
   - Each bullet should be 5-15 words
   - Each bullet must be directly derived from information in body_html
   - Each bullet should start with a capital letter and end without punctuation (unless it's a question)

STRICT COMPLIANCE GUIDELINES:
- NEVER make health claims (e.g., "cures", "treats", "prevents", "heals", "reduces symptoms")
- NEVER make medical claims (e.g., "FDA approved for", "clinically proven to cure")
- Use compliant language: "may help", "supports", "designed for" instead of definitive claims
- Avoid phrases that could trigger flags on Google Ads, Meta, Shopify, or payment processors
- Prioritize compliance over marketing flair
- If unsure about a claim, err on the side of caution and don't include it
- Focus on product features and ingredients, not therapeutic benefits
- Example: Say "Contains vitamin C" not "Vitamin C cures skin problems"
- Example: Say "Moisturizing formula" not "Eliminates wrinkles and fine lines"

ACCURACY GUIDELINES:
- NEVER add information that is not in the title or body_html
- NEVER assume product features, benefits, or specifications
- If body_html is empty or minimal, create a description based ONLY on the title
- If body_html has no extractable features, set bulletpoints to null or []
- Remove HTML tags and formatting from body_html when extracting information
- Work with the information you have - incomplete information is acceptable, hallucinated information is not
- Accuracy and truthfulness are the highest priorities
- If input lacks usable info, it's okay to have less content - no need to make things up

Return the data in the ProductContent BaseModel format.
"""


# Initialize LangChain components
llm = ChatAnthropic(model="claude-3-haiku-20240307")
parser = PydanticOutputParser(pydantic_object=ProductContent)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert e-commerce copywriter. You must ONLY use information provided in the product data. Do NOT hallucinate or invent information. Prioritize accuracy and compliance over marketing flair. Avoid health claims that could trigger platform flags. Format your response as JSON."),
    ("human", "{instructions}\n\nPRODUCT DATA:\nTitle: {title}\nBody HTML: {body_html}\n\nIMPORTANT: Only use information from the Title and Body HTML above. Do not add any information that is not explicitly stated. If information is missing, work with what you have. Accuracy is more important than completeness. Avoid health claims and prioritize compliance.\n\n{format_instructions}")
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

