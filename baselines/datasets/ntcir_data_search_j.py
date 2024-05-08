import os
import shutil
import bz2
import json
from huggingface_hub import hf_hub_download
from datasets import Dataset
from baselines.datasets.base import DatasetBase

class NtcirDataSearchJ(DatasetBase):

    def get_topics(self, filepath):
        self._download_and_copy(
            "mpkato/ntcir_data_search",
            "data_search_j_test_topics.tsv",
            filepath
        )

    def get_qrels(self, filepath):
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

    def get_docs(self, filepath):
        collection_filepath = hf_hub_download(
            repo_id="mpkato/ntcir_data_search", 
            filename="data_search_j_collection.jsonl.bz2", 
            repo_type="dataset"
        )
        def generate_doc_data():
            with bz2.open(collection_filepath, 'rt') as f:
                for line in f:
                    data = json.loads(line)
                    yield {
                        "id": data["id"],
                        "contents": "\n".join([data["title"], data["description"]]
                                            + list(data["data_fields"].values()))
                    }

        dataset = Dataset.from_generator(generate_doc_data)
        self.to_multi_jsonl(dataset, filepath)