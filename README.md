# Japanese IR Baselines 日本語情報検索ベースライン


## データセットの準備

```bash
$ poetry run python -m baselines.prepare_datasets \
  ntcir_data_search_j \
  datasets/ntcir_data_search_j
```

## 索引付け

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

## 検索

```bash
$ poetry run python -m pyserini.search.lucene \
  --index indexes/ntcir_data_search_j \
  --topics datasets/ntcir_data_search_j/test_topics.tsv \
  --output results/ntcir_data_search_j_bm25.trec \
  --language ja \
  --bm25
```

## 評価

```bash
$ poetry run ir_measures datasets/ntcir_data_search_j/qrels.txt results/ntcir_data_search_j_bm25.trec nDCG@10
```