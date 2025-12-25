/**
 * Product Content Generator API Client
 * 
 * Utility functions to call the Python FastAPI server from your Next.js app.
 * 
 * Usage:
 *   import { generateProductContent } from '@/lib/productContentApi';
 *   
 *   const content = await generateProductContent(title, bodyHtml);
 */

// Type definitions matching the Python API response
export interface ProductContent {
  displayName: string;
  displayDescription: string;
  bulletpoints: string[] | null;
}

export interface ProductContentRequest {
  title: string;
  body_html: string;
}

export interface ApiError {
  detail: string;
}

// API configuration
const API_BASE_URL =
  typeof window !== 'undefined' && (window as any).NEXT_PUBLIC_PRODUCT_API_URL
    ? (window as any).NEXT_PUBLIC_PRODUCT_API_URL
    : 'http://localhost:8000';

/**
 * Generate optimized product content from Shopify product data
 * 
 * @param title - Product title from Shopify
 * @param bodyHtml - Product description HTML (truncated at 'src=' to exclude images)
 * @returns Promise<ProductContent> - Generated product content
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * try {
 *   const content = await generateProductContent(
 *     'Turmeric & Vitamin C Cream -Lightweight Nourishment',
 *     '<h1>SPECIFICATIONS</h1><p>Feature: Moisturizing</p>'
 *   );
 *   console.log(content.displayName);
 * } catch (error) {
 *   console.error('Failed to generate content:', error);
 * }
 * ```
 */
export async function generateProductContent(
  title: string,
  bodyHtml: string
): Promise<ProductContent> {
  if (!title || !bodyHtml) {
    throw new Error('Title and body_html are required');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title,
        body_html: bodyHtml,
      }),
    });

    if (!response.ok) {
      const errorData: ApiError = await response.json().catch(() => ({
        detail: `HTTP error! status: ${response.status}`,
      }));
      throw new Error(errorData.detail || `API error: ${response.statusText}`);
    }

    const data: ProductContent = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred while generating product content');
  }
}

/**
 * Check if the API server is running and healthy
 * 
 * @returns Promise<boolean> - True if server is healthy
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Next.js API Route handler example
 * 
 * Place this in: app/api/product-content/route.ts (App Router)
 * or: pages/api/product-content.ts (Pages Router)
 * 
 * @example App Router (app/api/product-content/route.ts)
 * ```typescript
 * import { generateProductContent } from '@/lib/productContentApi';
 * import { NextRequest, NextResponse } from 'next/server';
 * 
 * export async function POST(request: NextRequest) {
 *   try {
 *     const { title, body_html } = await request.json();
 *     const content = await generateProductContent(title, body_html);
 *     return NextResponse.json(content);
 *   } catch (error) {
 *     return NextResponse.json(
 *       { error: error instanceof Error ? error.message : 'Unknown error' },
 *       { status: 500 }
 *     );
 *   }
 * }
 * ```
 */
