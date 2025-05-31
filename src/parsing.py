from docx import Document
import json
from utils import parse_articles
from argparse import ArgumentParser
import os
import sys

# add root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, required=True, default="test_cases")
    parser.add_argument("--output", type=str, required=True, default="test_cases/parsed")
    return parser.parse_args()

def parse_docx(input, output):
    if not os.path.exists(output):
        os.makedirs(output)

    docx_files = [f for f in os.listdir(input) if f.endswith('.docx')]
    for docx_file in docx_files:
        text = ""
        doc = Document(os.path.join(input, docx_file))
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        articles = parse_articles(text)

        with open(os.path.join(output, docx_file.replace('.docx', '.json')), 'w') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
    
    return text


def main(args):
    parse_docx(args.input, args.output)

if __name__ == "__main__":
    args = parse_args()
    main(args)