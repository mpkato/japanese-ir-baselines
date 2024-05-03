import os
import json
import logging
import hashlib
import shutil
from tqdm import tqdm
from datasets import Dataset
from dirhash import dirhash
from more_itertools import divide

class DatasetBase(object):

    FILENAMES = {
        "topics": "test_topics.tsv",
        "qrels": "test_qrels.txt",
        "docs": "docs",
    }

    FUNCS = {
        "topics": "get_topics",
        "qrels": "get_qrels",
        "docs": "get_docs",
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(filename)s\t%(funcName)s\t%(lineno)d\t%(message)s\n',
            '%Y-%m-%dT%H:%M:%S'
        )
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    def prepare(self, args):
        filepaths = {rtype: os.path.join(args.output_dirpath, filename)
                    for rtype, filename in self.FILENAMES.items()}
        for rtype, filepath in filepaths.items():
            self.logger.info(f"{rtype}: {filepath}")
            if self.is_valid_file(filepath, self.MD5[rtype]):
                self.logger.info(f"{rtype} already exists; skip preparation")
            else:
                self._clean(filepath)
                getattr(self, self.FUNCS[rtype])(filepath)
    
    def _clean(self, filepath):
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)

    @classmethod
    def to_multi_jsonl(cls, dataset, dirpath, filename="docs_{:02d}.jsonl", num=10):
        os.makedirs(dirpath, exist_ok=True)
        n = dataset.num_rows
        batch_indexes = divide(num, range(n))
        pbar = tqdm(total=n)
        for batch_idx, batch_index in enumerate(batch_indexes):
            filepath = os.path.join(dirpath, filename.format(batch_idx+1))
            with open(filepath, "w") as f:
                for idx in batch_index:
                    f.write(json.dumps(dataset[idx]) + "\n")
                    pbar.update(1)

    @classmethod
    def is_valid_file(cls, filepath, expected_md5):
        if os.path.exists(filepath):
            actual_md5 = ""
            if os.path.isfile(filepath):
                actual_md5 = cls.filemd5(filepath)
            elif os.path.isdir(filepath):
                actual_md5 = dirhash(filepath, "md5")
            return expected_md5 == actual_md5
        return False
    

    @classmethod
    def filemd5(cls, filepath, block_size=2**20):
        with open(filepath, 'rb') as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()