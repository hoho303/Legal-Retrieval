from docx import Document
import re
import json
from underthesea import text_normalize

def parse_articles(text):
    # Pattern to match article titles and content
    pattern = r'Điều\s+(\d+)\.\s+([^\n]+)\n(.*?)(?=Điều\s+\d+\.|$)'
    
    # Find all matches
    matches = re.finditer(pattern, text, re.DOTALL)
    
    articles = {}
    
    for match in matches:
        article_num = match.group(1)
        title = match.group(2).strip()
        content = match.group(3).strip()
        
        content = legal_normalize(content)
        
        articles[f"dieu_{article_num}"] = {
            "title": title,
            "text": content
        }
    
    return articles

def legal_normalize(text):
    # Pattern to match currency values like "1.2m", "1.5b".
    currency_pattern = r'(\d+(?:\.\d+)?)\s*([kmb])'
    
    def convert_currency(match):
        number = float(match.group(1))
        unit = match.group(2).lower()
        
        # Convert to VND based on unit
        if unit == 'k':
            number *= 1000
        elif unit == 'm':
            number *= 1000000
        elif unit == 'b':
            number *= 1000000000
            
        # Format number with dots as thousand separators
        formatted_number = "{:,.0f}".format(number).replace(',', '.')
        
        return f"{formatted_number} VNĐ"
    
    # Replace all currency patterns in the text
    normalized_text = re.sub(currency_pattern, convert_currency, text)
    
    # # Remove special characters
    # normalized_text = re.sub(r'[^\w\s]', '', normalized_text).lower()

    # # underthesea normalize
    # normalized_text = text_normalize(normalized_text)
    return normalized_text

def chunk_with_overlap(text, chunk_size=100, overlap=20):
    if not text:
        return []
    
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size") 
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap
        
    return chunks