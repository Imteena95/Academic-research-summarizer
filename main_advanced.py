"""
Advanced Research Paper Summarizer
Supports arXiv, IEEE, ACM with section-aware parsing
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import PyPDF2
import requests
import re
from typing import Optional, Dict, List
from pydantic import BaseModel
import arxiv
from datetime import datetime
import json

app = FastAPI(title="Advanced Research Paper Summarizer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"


class PaperSection(BaseModel):
    """Represents a section of a research paper"""
    name: str
    content: str
    page_range: Optional[tuple] = None


class ResearchPaper(BaseModel):
    """Represents a parsed research paper"""
    title: str
    authors: List[str]
    abstract: str
    sections: Dict[str, str]
    full_text: str
    source: str  # "upload", "arxiv", "ieee", "acm"
    url: Optional[str] = None


class SummaryRequest(BaseModel):
    """Request for paper summary"""
    paper_id: str
    summary_level: str  # "eli5", "technical", "expert"
    include_figures: bool = False
    include_methodology: bool = True


# Section patterns for academic papers
SECTION_PATTERNS = {
    "abstract": r"(?i)(abstract|summary)\s*\n",
    "introduction": r"(?i)(1\.|introduction|background)\s*\n",
    "methodology": r"(?i)(2\.|methodology|methods|approach|proposed method)\s*\n",
    "results": r"(?i)(3\.|results|findings|experiments|evaluation)\s*\n",
    "discussion": r"(?i)(4\.|discussion|analysis)\s*\n",
    "conclusion": r"(?i)(5\.|conclusion|conclusions|future work)\s*\n",
    "references": r"(?i)(references|bibliography)\s*\n",
}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def parse_paper_sections(text: str) -> Dict[str, str]:
    """Parse paper into sections using pattern matching."""
    sections = {}
    
    # Try to find each section
    for section_name, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            start = match.start()
            # Find next section
            next_start = len(text)
            for other_pattern in SECTION_PATTERNS.values():
                if other_pattern != pattern:
                    other_match = re.search(other_pattern, text[start+1:])
                    if other_match:
                        next_start = min(next_start, start + 1 + other_match.start())
            
            sections[section_name] = text[start:next_start].strip()
    
    return sections


def extract_metadata(text: str) -> Dict:
    """Extract paper metadata (title, authors, etc.)."""
    lines = text.split('\n')
    
    # First non-empty line is likely the title
    title = ""
    authors = []
    
    for line in lines[:20]:
        if line.strip() and len(line.strip()) > 10:
            if not title:
                title = line.strip()
            elif "author" in line.lower() or "@" in line:
                authors.append(line.strip())
    
    return {
        "title": title,
        "authors": authors,
    }


def fetch_arxiv_paper(arxiv_id: str) -> ResearchPaper:
    """Fetch paper from arXiv."""
    try:
        client = arxiv.Client()
        paper = next(client.results(arxiv.Search(id_list=[arxiv_id])))
        
        # Download PDF
        paper.download_pdf(dirpath=UPLOAD_DIR)
        pdf_path = os.path.join(UPLOAD_DIR, f"{arxiv_id}.pdf")
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        sections = parse_paper_sections(text)
        
        return ResearchPaper(
            title=paper.title,
            authors=[author.name for author in paper.authors],
            abstract=paper.summary,
            sections=sections,
            full_text=text,
            source="arxiv",
            url=paper.entry_id
        )
    except Exception as e:
        raise Exception(f"Error fetching arXiv paper: {str(e)}")


def summarize_section(section_text: str, section_name: str, summary_level: str) -> str:
    """Summarize a specific section using Ollama."""
    try:
        prompts = {
            "eli5": f"Explain this {section_name} section in simple terms a 5-year-old could understand:\n{section_text[:2000]}",
            "technical": f"Provide a technical summary of this {section_name} section:\n{section_text[:2000]}",
            "expert": f"Provide an expert-level analysis of this {section_name} section:\n{section_text[:2000]}"
        }
        
        prompt = prompts.get(summary_level, prompts["technical"])
        
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "orca-mini",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            raise Exception(f"Ollama error: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error summarizing section: {str(e)}")


def generate_multi_level_summary(paper: ResearchPaper, summary_level: str) -> Dict:
    """Generate multi-level summary of paper."""
    try:
        summaries = {}
        
        # Summarize key sections
        key_sections = ["abstract", "introduction", "methodology", "results", "conclusion"]
        
        for section in key_sections:
            if section in paper.sections:
                summaries[section] = summarize_section(
                    paper.sections[section],
                    section,
                    summary_level
                )
        
        return summaries
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")


def extract_key_figures(text: str) -> List[str]:
    """Extract references to figures and tables."""
    figures = re.findall(r"(?i)(figure|fig\.|table|tbl\.)\s+(\d+[a-z]?)", text)
    return [f"{fig[0]} {fig[1]}" for fig in figures]


def generate_methodology_recreation(paper: ResearchPaper) -> str:
    """Generate a recreation of the methodology section."""
    if "methodology" in paper.sections:
        return summarize_section(
            paper.sections["methodology"],
            "methodology",
            "technical"
        )
    return "Methodology section not found"


def suggest_related_work(paper: ResearchPaper) -> List[str]:
    """Suggest related papers based on keywords."""
    try:
        # Extract keywords from abstract and introduction
        text = paper.abstract + " " + paper.sections.get("introduction", "")
        
        # Simple keyword extraction
        keywords = re.findall(r"\b[a-z]{4,}\b", text.lower())
        keywords = list(set(keywords))[:5]
        
        # Search arXiv for related papers
        related = []
        client = arxiv.Client()
        
        for keyword in keywords:
            try:
                search = arxiv.Search(query=keyword, max_results=2)
                for result in client.results(search):
                    related.append({
                        "title": result.title,
                        "authors": [a.name for a in result.authors],
                        "arxiv_id": result.entry_id.split('/abs/')[-1]
                    })
            except:
                pass
        
        return related[:5]
    except Exception as e:
        return []


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Advanced Research Paper Summarizer",
        "features": [
            "Section-aware parsing",
            "Multi-level summaries (ELI5, technical, expert)",
            "arXiv integration",
            "Figure extraction",
            "Methodology recreation",
            "Related work suggestions"
        ]
    }


@app.post("/upload-paper")
async def upload_paper(file: UploadFile = File(...)):
    """Upload and parse a research paper."""
    file_path = None
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Extract text
        text = extract_text_from_pdf(file_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse sections
        sections = parse_paper_sections(text)
        metadata = extract_metadata(text)
        
        # Extract figures
        figures = extract_key_figures(text)
        
        paper_id = file.filename.replace('.pdf', '')
        
        return JSONResponse({
            "status": "success",
            "paper_id": paper_id,
            "title": metadata.get("title", "Unknown"),
            "authors": metadata.get("authors", []),
            "sections": list(sections.keys()),
            "figures": figures,
            "text_length": len(text),
            "page_count": len(PyPDF2.PdfReader(file_path).pages)
        })
    
    except HTTPException:
        raise
    except Exception as e:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/arxiv-paper")
async def fetch_arxiv(arxiv_id: str):
    """Fetch and parse paper from arXiv."""
    try:
        paper = fetch_arxiv_paper(arxiv_id)
        
        return JSONResponse({
            "status": "success",
            "paper_id": arxiv_id,
            "title": paper.title,
            "authors": paper.authors,
            "abstract": paper.abstract,
            "sections": list(paper.sections.keys()),
            "source": "arxiv",
            "url": paper.url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize")
async def summarize_paper(request: SummaryRequest):
    """Generate multi-level summary of paper."""
    try:
        # Load paper from file
        file_path = os.path.join(UPLOAD_DIR, f"{request.paper_id}.pdf")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Paper not found")
        
        # Extract and parse
        text = extract_text_from_pdf(file_path)
        sections = parse_paper_sections(text)
        metadata = extract_metadata(text)
        
        paper = ResearchPaper(
            title=metadata.get("title", "Unknown"),
            authors=metadata.get("authors", []),
            abstract=sections.get("abstract", ""),
            sections=sections,
            full_text=text,
            source="upload"
        )
        
        # Generate summaries
        summaries = generate_multi_level_summary(paper, request.summary_level)
        
        result = {
            "status": "success",
            "paper_id": request.paper_id,
            "summary_level": request.summary_level,
            "summaries": summaries,
        }
        
        if request.include_figures:
            result["figures"] = extract_key_figures(text)
        
        if request.include_methodology:
            result["methodology"] = generate_methodology_recreation(paper)
        
        return JSONResponse(result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/related-work/{paper_id}")
async def get_related_work(paper_id: str):
    """Get related work suggestions."""
    try:
        file_path = os.path.join(UPLOAD_DIR, f"{paper_id}.pdf")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Paper not found")
        
        text = extract_text_from_pdf(file_path)
        sections = parse_paper_sections(text)
        metadata = extract_metadata(text)
        
        paper = ResearchPaper(
            title=metadata.get("title", "Unknown"),
            authors=metadata.get("authors", []),
            abstract=sections.get("abstract", ""),
            sections=sections,
            full_text=text,
            source="upload"
        )
        
        related = suggest_related_work(paper)
        
        return JSONResponse({
            "status": "success",
            "paper_id": paper_id,
            "related_papers": related
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
