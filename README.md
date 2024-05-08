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

## MIRACL (日本語，dev)

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

### データセットの入手

1. [NTCIR-1: 情報検索／用語抽出研究用テストコレクション](https://research.nii.ac.jp/ntcir/permission/perm-ja.html#ntcir-1)から「テストコレクション利用申込書」にしたがって利用申込を行う
2. 得られたZipファイルを解凍して`MLIR.TGZ`と`TOPICS.TGZ`を`original_data/NTCIR-1/`以下などに展開しておく
3. 以下のファイルを読み込めることを`less`コマンドなどで確認しておく（違う場所に展開されている場合には`config.yaml`ファイルの設定を変更しても良い）

- `original_data/NTCIR-1/topics/topic0031-0083`
- `original_data/NTCIR-1/mlir/rel2_ntc1-j1_0031-0083`
- `original_data/NTCIR-1/mlir/ntc1-j1`


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


## NTCIR-2 単言語検索（日本語，test）

### データセットの入手

NTCIR-2はNTCIR-1の文書コレクションを含むためNTCIR-1の利用申込も必要となる．

1. [NTCIR-1: 情報検索／用語抽出研究用テストコレクション](https://research.nii.ac.jp/ntcir/permission/perm-ja.html#ntcir-1)，および，[NTCIR-2: 情報検索用テストコレクション](https://research.nii.ac.jp/ntcir/permission/perm-ja.html#ntcir-2)から「テストコレクション利用申込書」にしたがって利用申込を行う
2. NTCIR-1のZipファイルを解凍して`MLIR.TGZ`を`original_data/NTCIR-1/`以下などに展開しておく．
3. NTCIR-2のZipファイルを解凍して`j-docs.tgz`，`topics.tgz`，`rels.tgz`を`original_data/NTCIR-2/`以下などに展開しておく．
4. 以下のファイルを読み込めることを`less`コマンドなどで確認しておく（違う場所に展開されている場合には`config.yaml`ファイルの設定を変更しても良い）

- `original_data/NTCIR-1/mlir/ntc1-j1`
- `original_data/NTCIR-2/j-docs/ntc2-j1g`
- `original_data/NTCIR-2/j-docs/ntc2-j1k`
- `original_data/NTCIR-2/topics/topic-j0101-0149`
- `original_data/NTCIR-2/rels/rel2_ntc2-j2_0101-0149`


### データセットの準備

```bash
$ poetry run python -m baselines.prepare_dataset \
  ntcir_2_j \
  datasets/ntcir_2_j
```

### 索引付け

```bash
$ poetry run python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input datasets/ntcir_2_j/docs \
  --language ja \
  --index indexes/ntcir_2_j \
  --generator DefaultLuceneDocumentGenerator \
  --threads 10 \
  --storePositions --storeDocvectors --storeRaw
```

### 検索

```bash
$ poetry run python -m pyserini.search.lucene \
  --index indexes/ntcir_2_j \
  --topics datasets/ntcir_2_j/test_topics.tsv \
  --output results/ntcir_2_j_bm25.trec \
  --language ja \
  --bm25
```

### 評価

```bash
$ poetry run ir_measures datasets/ntcir_2_j/test_qrels.txt results/ntcir_2_j_bm25.trec nDCG@10
```