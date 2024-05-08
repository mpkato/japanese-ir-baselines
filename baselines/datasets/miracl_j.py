import os
import shutil
import bz2
import json
from huggingface_hub import hf_hub_download
from datasets import Dataset, load_dataset
from baselines.datasets.base import DatasetBase

class MiraclJ(DatasetBase):

    MD5 = {
        "topics": "e12d168a19103822f145d7f16c1a4b57",
        "qrels": "c03cbb9ae5c610f7a4bf9d119be77e04",
        "docs": "cd53a68cc3230663b56f88d953f2fa8b",
    }

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