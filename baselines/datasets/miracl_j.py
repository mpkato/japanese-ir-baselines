import os
import shutil
import bz2
import json
from huggingface_hub import hf_hub_download
from datasets import Dataset, load_dataset
from baselines.datasets.base import DatasetBase

class MiraclJ(DatasetBase):

    def get_topics(self, filepath):
        self._download_and_copy(
            "miracl/miracl", 
            "miracl-v1.0-ja/topics/topics.miracl-v1.0-ja-dev.tsv", 
            filepath
        )

    def get_qrels(self, filepath):
        self._download_and_copy(
            "miracl/miracl", 
            "miracl-v1.0-ja/qrels/qrels.miracl-v1.0-ja-dev.tsv", 
            filepath
        )

    def get_docs(self, filepath):
        original_dataset = load_dataset("miracl/miracl-corpus", "ja",
                                        trust_remote_code=True)
        new_dataset = original_dataset.map(
            lambda row: {"id": row["docid"], "contents": f'{row["title"]}\n{row["text"]}'}, 
            remove_columns=["docid", "title", "text"], num_proc=self.num_proc)['train']
        self.to_multi_jsonl(new_dataset, filepath)