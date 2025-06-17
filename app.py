import os
import json
import base64
import logging
from io import BytesIO
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from PIL import Image
from xhtml2pdf import pisa

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="PDF Splitter API",
    description="API para dividir PDFs e converter HTML para PDF",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Pydantic models for request/response validation
class PDFSplitRequest(BaseModel):
    pdf_base64: str = Field(..., description="Base64 encoded PDF data")

class HTMLToPDFRequest(BaseModel):
    html_content: str = Field(..., description="HTML content to convert to PDF")

class PageData(BaseModel):
    page_number: int
    pdf_base64: Optional[str] = None
    image_base64: Optional[str] = None

class PDFSplitResponse(BaseModel):
    success: bool
    pages: List[PageData]
    total_pages: int
    error: Optional[str] = None

class HTMLToPDFResponse(BaseModel):
    success: bool
    pdf_base64: Optional[str] = None
    pages: List[PageData]
    total_pages: int
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page with PDF upload form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/split-pdf", response_model=PDFSplitResponse)
async def split_pdf(request: PDFSplitRequest):
    """
    API endpoint to split PDF pages and return base64-encoded individual pages.
    
    Args:
        request: PDFSplitRequest containing base64-encoded PDF data
    
    Returns:
        PDFSplitResponse with individual pages data
    """
    try:
        pdf_base64 = request.pdf_base64
        
        if not pdf_base64:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'pdf_base64' field cannot be empty"
            )
        
        # Decode base64 PDF data
        try:
            pdf_data = base64.b64decode(pdf_base64)
        except Exception as e:
            logger.error(f"Base64 decode error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 encoding"
            )
        
        # Create PDF reader from decoded data
        try:
            pdf_stream = BytesIO(pdf_data)
            pdf_reader = PdfReader(pdf_stream)
        except Exception as e:
            logger.error(f"PDF reading error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PDF file or corrupted data"
            )
        
        # Check if PDF has pages
        if len(pdf_reader.pages) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PDF file contains no pages"
            )
        
        # Convert PDF to images first
        try:
            images = convert_from_bytes(pdf_data, dpi=200, fmt='PNG')
            logger.debug(f"Successfully converted PDF to {len(images)} images")
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting PDF to images: {str(e)}"
            )

        # Split PDF into individual pages and convert to images
        pages_data = []
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                # Create a new PDF writer for this page
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                
                # Write the single page to a BytesIO buffer
                page_buffer = BytesIO()
                pdf_writer.write(page_buffer)
                page_buffer.seek(0)
                
                # Encode the page as base64
                page_base64 = base64.b64encode(page_buffer.getvalue()).decode('utf-8')
                
                # Convert corresponding image to base64
                image_base64 = None
                if page_num <= len(images):
                    image = images[page_num - 1]  # 0-indexed
                    image_buffer = BytesIO()
                    image.save(image_buffer, format='PNG')
                    image_buffer.seek(0)
                    image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
                
                pages_data.append(PageData(
                    page_number=page_num,
                    pdf_base64=page_base64,
                    image_base64=image_base64
                ))
                
                logger.debug(f"Successfully processed page {page_num}")
                
            except Exception as e:
                logger.error(f"Error processing page {page_num}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error processing page {page_num}: {str(e)}"
                )
        
        # Return successful response
        logger.info(f"Successfully split PDF into {len(pages_data)} pages")
        return PDFSplitResponse(
            success=True,
            pages=pages_data,
            total_pages=len(pages_data)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in split_pdf: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/api/html-to-pdf", response_model=HTMLToPDFResponse)
async def html_to_pdf(request: HTMLToPDFRequest):
    """
    API endpoint to convert HTML to PDF and return base64-encoded PDF and images.
    
    Args:
        request: HTMLToPDFRequest containing HTML content
    
    Returns:
        HTMLToPDFResponse with PDF and page images data
    """
    try:
        html_content = request.html_content
        
        if not html_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'html_content' field cannot be empty"
            )
        
        # Convert HTML to PDF using xhtml2pdf
        try:
            logger.debug("Converting HTML to PDF...")
            pdf_buffer = BytesIO()
            
            # Create PDF from HTML
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=pdf_buffer
            )
            
            if pisa_status.err:
                logger.error(f"xhtml2pdf error: {pisa_status.err}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error converting HTML to PDF"
                )
            
            # Get PDF bytes
            pdf_buffer.seek(0)
            pdf_data = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            if len(pdf_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Generated PDF is empty"
                )
            
            # Encode PDF as base64
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            
            logger.debug(f"Successfully converted HTML to PDF ({len(pdf_data)} bytes)")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"HTML to PDF conversion error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting HTML to PDF: {str(e)}"
            )
        
        # Convert PDF to images for each page
        try:
            images = convert_from_bytes(pdf_data, dpi=200, fmt='PNG')
            logger.debug(f"Successfully converted PDF to {len(images)} images")
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting PDF to images: {str(e)}"
            )
        
        # Process each page image
        pages_data = []
        
        for page_num, image in enumerate(images, 1):
            try:
                # Convert image to base64
                image_buffer = BytesIO()
                image.save(image_buffer, format='PNG')
                image_buffer.seek(0)
                image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
                
                pages_data.append(PageData(
                    page_number=page_num,
                    image_base64=image_base64
                ))
                
                logger.debug(f"Successfully processed page {page_num} image")
                
            except Exception as e:
                logger.error(f"Error processing page {page_num} image: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error processing page {page_num} image: {str(e)}"
                )
        
        # Return successful response
        logger.info(f"Successfully converted HTML to PDF with {len(pages_data)} pages")
        return HTMLToPDFResponse(
            success=True,
            pdf_base64=pdf_base64,
            pages=pages_data,
            total_pages=len(pages_data)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in html_to_pdf: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

# Exception handlers for custom error responses
@app.exception_handler(413)
async def request_entity_too_large_handler(request: Request, exc):
    """Handle file too large errors."""
    return JSONResponse(
        status_code=413,
        content={
            "success": False,
            "error": "File too large. Please upload a smaller PDF file."
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found"
        }
    )

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    """Handle method not allowed errors."""
    return JSONResponse(
        status_code=405,
        content={
            "success": False,
            "error": "Method not allowed"
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "PDF Splitter API"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="info")
