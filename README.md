# Japanese IR Baselines 日本語情報検索ベースライン

## NTCIR Data Search 1 (日本語，test)

### データセットの準備

```bash
$ poetry run python -m baselines.prepare_dataset \
  ntcir_data_search_j \
  datasets/ntcir_data_search_j
```

### 索引付け

```bash
$ poetry run python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input datasets/ntcir_data_search_j/docs \
  --language ja \
  --index indexes/ntcir_data_search_j \
  --generator DefaultLuceneDocumentGenerator \
  --threads 10 \
  --storePositions --storeDocvectors --storeRaw
```

### 検索

```bash
$ poetry run python -m pyserini.search.lucene \
  --index indexes/ntcir_data_search_j \
  --topics datasets/ntcir_data_search_j/test_topics.tsv \
  --output results/ntcir_data_search_j_bm25.trec \
  --language ja \
  --bm25
```

### 評価

```bash
$ poetry run ir_measures datasets/ntcir_data_search_j/test_qrels.txt results/ntcir_data_search_j_bm25.trec nDCG@10
```

## MIRAC (日本語，dev)

### データセットの準備

```bash
$ poetry run python -m baselines.prepare_dataset \
  miracl_j \
  datasets/miracl_j
```

### 索引付け

```bash
$ poetry run python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input datasets/miracl_j/docs \
  --language ja \
  --index indexes/miracl_j \
  --generator DefaultLuceneDocumentGenerator \
  --threads 10 \
  --storePositions --storeDocvectors --storeRaw
```

### 検索

```bash
$ poetry run python -m pyserini.search.lucene \
  --index indexes/miracl_j \
  --topics datasets/miracl_j/test_topics.tsv \
  --output results/miracl_j_bm25.trec \
  --language ja \
  --bm25
```

### 評価

```bash
$ poetry run ir_measures datasets/miracl_j/test_qrels.txt results/miracl_j_bm25.trec nDCG@10
```

## NTCIR-1 単言語検索（日本語，test）

### データセットの準備

```bash
$ poetry run python -m baselines.prepare_dataset \
  ntcir_1_j \
  datasets/ntcir_1_j
```

### 索引付け

```bash
$ poetry run python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input datasets/ntcir_1_j/docs \
  --language ja \
  --index indexes/ntcir_1_j \
  --generator DefaultLuceneDocumentGenerator \
  --threads 10 \
  --storePositions --storeDocvectors --storeRaw
```

### 検索

```bash
$ poetry run python -m pyserini.search.lucene \
  --index indexes/ntcir_1_j \
  --topics datasets/ntcir_1_j/test_topics.tsv \
  --output results/ntcir_1_j_bm25.trec \
  --language ja \
  --bm25
```

### 評価

```bash
$ poetry run ir_measures datasets/ntcir_1_j/test_qrels.txt results/ntcir_1_j_bm25.trec nDCG@10
```