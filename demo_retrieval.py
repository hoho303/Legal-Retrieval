from src.retrieval import LegalRetrieval
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_dir", type=str, help="Directory containing JSON files", default="articles_parsing/")
    parser.add_argument("--query", type=str, help="Search query", default="NLĐ bị sa thải có được trả lương hay không?")
    parser.add_argument("--k", type=int, default=5, help="Number of results to return")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Initialize retrieval system
    retriever = LegalRetrieval()
    
    # Build embeddings
    print("Building embeddings...")
    retriever.build_embeddings(args.json_dir)
    
    # Search
    print(f"\nSearching for: {args.query}")
    results = retriever.search(args.query, k=args.k)
    
    # Print results
    print("\nResults:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['id']} (Score: {result['score']:.4f})")
        print(f"Title: {result['title']}")
        print(f"Text: {result['text'][:200]}...")
        print(f"File: {result['file']}")

if __name__ == "__main__":
    main() 