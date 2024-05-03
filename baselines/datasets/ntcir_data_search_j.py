import os
import shutil
import bz2
import json
from huggingface_hub import hf_hub_download
from datasets import Dataset

def ntcir_data_search_j(args):
    topics_filepath = os.path.join(args.output_dirpath, "test", "topics.tsv")
    qrels_filepath = os.path.join(args.output_dirpath, "qrels.txt")
    corpus_filepath = os.path.join(args.output_dirpath, "corpus", "ntcir_data_search_j.jsonl")

    filepath_to_func = {
        topics_filepath: ntcir_data_search_j_topics,
        qrels_filepath: ntcir_data_search_j_qrels,
        corpus_filepath: ntcir_data_search_j_corpus,
    }
    for filepath, func in filepath_to_func.items():
        if not os.path.exists(filepath):
            func(filepath)
            print(f"{func.__name__}: {filepath}")

def ntcir_data_search_j_topics(filepath):
    collection_filepath = hf_hub_download(
        repo_id="mpkato/ntcir_data_search", 
        filename="data_search_j_test_topics.tsv", 
        repo_type="dataset"
    )
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    shutil.copyfile(collection_filepath, filepath)

def ntcir_data_search_j_qrels(filepath):
    collection_filepath = hf_hub_download(
        repo_id="mpkato/ntcir_data_search", 
        filename="data_search_j_test_qrels.txt", 
        repo_type="dataset"
    )
    def generate_qrels():
        with open(collection_filepath) as f:
            for line in f:
                qid, did, rel_level = line.split(" ")
                # There is a prefix "L" in rel_level. Remove it, e.g., "L1" -> "1".
                grade = int(rel_level[1:]) 
                yield {
                    "qid": qid,
                    "Q0": "Q0",
                    "did": did,
                    "grade": grade
                }

    dataset = Dataset.from_generator(generate_qrels)
    dataset.to_csv(filepath, sep=' ', index=None, header=None)

def ntcir_data_search_j_corpus(filepath):
    collection_filepath = hf_hub_download(
        repo_id="mpkato/ntcir_data_search", 
        filename="data_search_j_collection.jsonl.bz2", 
        repo_type="dataset"
    )
    def generate_corpus_data():
        with bz2.open(collection_filepath, 'rt') as f:
            for line in f:
                data = json.loads(line)
                yield {
                    "id": data["id"],
                    "contents": "\n".join([data["title"], data["description"]]
                                          + list(data["data_fields"].values()))
                }

    dataset = Dataset.from_generator(generate_corpus_data)
    dataset.to_json(filepath)