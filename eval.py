import json
import numpy as np
from typing import List, Union
from src.retrieval import LegalRetrieval
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_dir", type=str, help="Directory containing JSON files", default="articles_parsing/")
    parser.add_argument("--k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--qa_file", type=str, help="Output file", default="data/legal_QA.json")
    return parser.parse_args()

def calculate_mrr(relevant_docs: List[List[dict]], retrieved_docs: List[List[dict]], k: int = None) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR) for a retrieval system.
    """
    
    reciprocal_ranks = []
    
    for query_relevant, query_retrieved in zip(relevant_docs, retrieved_docs):
        if k is not None:
            query_retrieved = query_retrieved[:k]
        
        # Find the rank of the first relevant document
        for rank, doc_id in enumerate(query_retrieved, start=1):
            if doc_id['id'] in query_relevant['gid'] and doc_id['file'] == query_relevant['file']:
                reciprocal_ranks.append(1.0 / rank)
                break
        else:
            reciprocal_ranks.append(0.0)
    
    mrr = np.mean(reciprocal_ranks)
    return mrr

def main(args):
    # Initialize retrieval system
    retriever = LegalRetrieval()
    
    # Build embeddings
    print("Building embeddings...")
    retriever.build_embeddings(args.json_dir)
    
    # Load questions
    with open(args.qa_file, "r") as f:
        data = json.load(f)
    questions = data["questions"]
    
    all_results = []
    for question in questions:
        # Search
        print(f"\nSearching for: {question['question']}")
        results = retriever.search(question['question'], k=args.k)
        all_results.append(results)
    
    mrr = calculate_mrr(questions, all_results, k=args.k)
    print(f"MRR: {mrr}")

if __name__ == "__main__":
    args = parse_args()
    main(args)    
