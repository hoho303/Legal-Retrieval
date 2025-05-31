# Legal Retrieval
Demo of legal retrieval system using PhoBERT embeddings and FastAPI.

## Install
```
pip install -r requirements.txt
```

## Parsing Data
- Convert data from Docx to JSON.
- Normalize data with Vietnamese currency format.
```
python src/parsing.py --input data --output articles_parsing/
```

## Demo
```
python demo_retrieval.py --json_dir articles_parsing/ --query "NLĐ bị sa thải có được trả lương hay không?" --k 5
```

Run server API
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Evaluate
Evaluate the retrieval system using Mean Reciprocal Rank (MRR) metric.
```
python eval.py --json_dir articles_parsing/ --qa_file data/legal_QA.json --k 5
```

## Docker
Build Docker Image
```
docker build -t legal-retrieval .
```

Run Docker Container
```
docker run -d -p 8000:8000 legal-retrieval
```

Live preview: http://146.148.98.227:8000/