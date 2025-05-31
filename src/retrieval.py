import json
import os
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
import torch
from underthesea import word_tokenize
from src.utils import chunk_with_overlap

class LegalRetrieval:
    def __init__(self, model_name="vinai/phobert-base-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        # self.index = faiss.IndexFlatL2(768)
        self.embeddings = []
        self.documents = []
        
    def get_embedding(self, text):
        text = word_tokenize(text, format="text")
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        try:
            with torch.no_grad():
                outputs = self.model(**inputs)
        except Exception as e:
            print(f"Error getting embedding: {e}")
            print(f"Error text: {text}")
            return None
        
        embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        return embeddings[0]
    
    def build_embeddings(self, json_dir):
        """        
        Args:
            json_dir (str): Directory containing JSON files
            batch_size (int): Number of documents to process in each batch
        """
        import tqdm
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        self.documents = []
        # all_embeddings = []

        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        
        for filename in tqdm.tqdm(json_files, desc="Processing files"):
            try:
                with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for id, content in data.items():
                    chunks = chunk_with_overlap(content["text"], chunk_size=400, overlap=30)
                    for chunk in chunks:
                        full_text = f"{content['title']} {chunk}"
                        embeddings = self.get_embedding(full_text)
                        self.embeddings.append(embeddings)
                        
                        self.documents.append({
                            'id': id,
                            'title': content['title'],
                            'text': chunk,
                            'file': filename.replace('.json', '')
                        })
                            
            except Exception as e:
                logger.error(f"Error processing file {filename}: {str(e)}")
                continue
            
        # self.index.add(np.array(all_embeddings))
    def search(self, query, k=5):
        """
        Search for most similar documents using cosine similarity
        
        """

        if not self.embeddings:
            raise ValueError("No embeddings available. Call build_embeddings first.")
        
        query_embedding = self.get_embedding(query)
        if query_embedding is None:
            return []
            
        query_embedding = np.array(query_embedding)
        
        # Calculate cosine similarity with all documents
        similarities = []
        for doc_embedding in self.embeddings:
            # Normalize vectors
            query_norm = query_embedding / np.linalg.norm(query_embedding)
            doc_norm = doc_embedding / np.linalg.norm(doc_embedding)
            # Calculate cosine similarity
            similarity = np.dot(query_norm, doc_norm)
            similarities.append(similarity)
            
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            results.append({
                'id': self.documents[idx]['id'],
                'title': self.documents[idx]['title'],
                'text': self.documents[idx]['text'],
                'file': self.documents[idx]['file'],
                'score': float(similarities[idx])
            })
        
        return results 